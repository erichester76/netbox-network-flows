from scapy.all import sniff, IP, TCP, UDP
import time
import sqlite3
import threading
import requests
import socket
import os
import netifaces
import ipaddress
from collections import defaultdict
import logging

# Configuration
NETBOX_URL = "https://o11y.dev.clemson.edu/netbox/api/plugins/flows/flows/"
NETBOX_TOKEN = "25c89f4320476edf29a6cb24a1d2b085b1fd5264"
DB_PATH = "/tmp/local_flows.db"
LOG_FILE = "/var/log/traffic_agent.log"

EPHEMERAL_PORT_MIN = 10000
SERVICE_PORT_THRESHOLD = 4

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

SERVER_ID = socket.gethostname().split('.')[0]
logger.info(f"Determined SERVER_ID as {SERVER_ID}")

def get_interfaces_and_subnets():
    interfaces, subnets = [], []
    physical_ip = None
    for iface in netifaces.interfaces():
        if iface == "lo" or iface.startswith(('docker', 'br-', 'veth', 'virbr')):
            logger.debug(f"Skipping virtual interface: {iface}")
            continue
        if not iface.startswith('e'):
            logger.debug(f"Skipping non-Ethernet interface: {iface}")
            continue
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr["addr"]
                netmask = addr["netmask"]
                try:
                    network = ipaddress.ip_network(f"{ip}/{netmask}", strict=False)
                    interfaces.append(iface)
                    subnets.append(str(network))
                    logger.debug(f"Found physical interface {iface} with IP {ip} and subnet {network}")
                    if not physical_ip:  # Take first physical IP as replacement
                        physical_ip = ip
                except ValueError as e:
                    logger.warning(f"Skipping invalid IP config on {iface}: {e}")
    return interfaces, subnets, physical_ip

INTERFACES, SUBNETS, PHYSICAL_IP = get_interfaces_and_subnets()
if not INTERFACES:
    logger.error("No valid network interfaces found. Exiting.")
    exit(1)
if not PHYSICAL_IP:
    logger.error("No physical IP found for substitution. Exiting.")
    exit(1)

INTERFACES.append('lo')
FILTER = " or ".join(f"net {subnet}" for subnet in SUBNETS) + " or net 127.0.0.0/8"
logger.info(f"Constructed filter: {FILTER}")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flows'")
if cursor.fetchone():
    cursor.execute("PRAGMA table_info(flows)")
    columns = [col[1] for col in cursor.fetchall()]
    required_columns = {'src_ip', 'dst_ip', 'proto', 'service_port', 'server_id', 'timestamp', 'written_to_netbox'}
    if not required_columns.issubset(columns):
        cursor.execute("DROP TABLE flows")
        cursor.execute('''CREATE TABLE flows
                        (src_ip TEXT, dst_ip TEXT, proto TEXT, service_port INT, server_id TEXT, timestamp REAL, written_to_netbox INTEGER DEFAULT 0)''')
        logger.info("Recreated flows table with new schema")
else:
    cursor.execute('''CREATE TABLE flows
                    (src_ip TEXT, dst_ip TEXT, proto TEXT, service_port INT, server_id TEXT, timestamp REAL, written_to_netbox INTEGER DEFAULT 0)''')
conn.commit()

unique_flows = set()
port_connections = defaultdict(lambda: {'src_ports': set(), 'dst_ports': set()})

def load_existing_flows():
    global unique_flows
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT src_ip, dst_ip, proto, service_port FROM flows")
    existing_flows = cursor.fetchall()
    for flow in existing_flows:
        src_ip, dst_ip, proto_name, service_port = flow
        unique_flow = (src_ip, dst_ip, proto_name, service_port)
        unique_flows.add(unique_flow)
    logger.info(f"Loaded {len(unique_flows)} unique flows from local database")

def process_packet(packet):
    try:
        if IP not in packet:
            logger.debug("Packet skipped: No IP layer present")
            return

        ip = packet[IP]
        src_ip = ip.src
        dst_ip = ip.dst
        proto = ip.proto
        src_port = dst_port = 0

        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            proto_name = "tcp"
        elif UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            proto_name = "udp"
        else:
            proto_name = str(proto)

        # Replace 127.0.0.1 with physical IP for lo0 flows
        if src_ip == "127.0.0.1":
            src_ip = PHYSICAL_IP
        if dst_ip == "127.0.0.1":
            dst_ip = PHYSICAL_IP

        # Track connections
        port_connections[(dst_ip, dst_port)]['src_ports'].add(src_port)
        port_connections[(src_ip, src_port)]['dst_ports'].add(dst_port)

        # Determine service port and ensure it's stored as dst_port
        if len(port_connections[(dst_ip, dst_port)]['src_ports']) >= SERVICE_PORT_THRESHOLD:
            store_src_ip = src_ip
            store_dst_ip = dst_ip
            service_port = dst_port
        elif len(port_connections[(src_ip, src_port)]['dst_ports']) >= SERVICE_PORT_THRESHOLD:
            store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
            store_dst_ip = src_ip
            service_port = src_port
        elif src_port < EPHEMERAL_PORT_MIN and dst_port < EPHEMERAL_PORT_MIN:
            if src_port < dst_port:
                store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
                store_dst_ip = src_ip
                service_port = src_port
            else:
                store_src_ip = src_ip
                store_dst_ip = dst_ip
                service_port = dst_port
        elif dst_port < EPHEMERAL_PORT_MIN:
            store_src_ip = src_ip
            store_dst_ip = dst_ip
            service_port = dst_port
        elif src_port < EPHEMERAL_PORT_MIN:
            store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
            store_dst_ip = src_ip
            service_port = src_port
        else:
            logger.debug(f"Skipping flow, no clear service port: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            return

        flow = (store_src_ip, store_dst_ip, proto_name, service_port)

        if flow not in unique_flows:
            unique_flows.add(flow)
            logger.info(f"New flow detected: {src_ip}:{src_port} -> {dst_ip}:{dst_port} (stored as {store_src_ip}->{store_dst_ip}:{service_port})")
            conn.execute("INSERT INTO flows (src_ip, dst_ip, proto, service_port, server_id, timestamp, written_to_netbox) VALUES (?, ?, ?, ?, ?, ?, 0)",
                         (store_src_ip, store_dst_ip, proto_name, service_port, SERVER_ID, time.time()))
            conn.commit()

    except Exception as e:
        logger.error(f"Error processing packet: {e}", exc_info=True)

def flush_to_db():
    pass

def send_to_netbox():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    while True:
        time.sleep(60)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT src_ip, dst_ip, proto, service_port, server_id, timestamp
                FROM flows
                WHERE written_to_netbox = 0
            """)
            flows = cursor.fetchall()
            if flows:
                new_flows_count = 0
                for flow in flows:
                    src_ip, dst_ip, proto_name, service_port, server_id, timestamp = flow
                    params = {
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'protocol': proto_name,
                        'service_port': service_port,
                        'server_id': server_id
                    }
                    check_key = (src_ip, dst_ip, proto_name, service_port)

                    logger.debug(f"Sending GET to {NETBOX_URL} with params: {params}")
                    check_response = requests.get(NETBOX_URL, headers=headers, params=params)
                    logger.debug(f"GET response: status={check_response.status_code}, body={check_response.text}")

                    if check_response.status_code == 200:
                        response_data = check_response.json()
                        results = response_data.get('results', [])
                        flow_exists = False
                        for result in results:
                            result_key = (
                                result['src_ip'],
                                result['dst_ip'],
                                result['protocol'],
                                result['service_port']
                            )
                            if result_key == check_key:
                                flow_exists = True
                                logger.debug(f"Flow {src_ip}:{service_port} -> {dst_ip} already exists in NetBox: {result}")
                                conn.execute("""
                                    UPDATE flows
                                    SET written_to_netbox = 1
                                    WHERE src_ip = ? AND dst_ip = ? AND proto = ? AND service_port = ? AND server_id = ? AND timestamp = ?
                                """, (src_ip, dst_ip, proto_name, service_port, server_id, timestamp))
                                conn.commit()
                                break

                        if not flow_exists:
                            flow_data = {
                                "src_ip": src_ip,
                                "dst_ip": dst_ip,
                                "protocol": proto_name,
                                "service_port": service_port,
                                "server_id": server_id,
                                "timestamp": float(timestamp)
                            }
                            logger.debug(f"Sending POST to {NETBOX_URL} with headers {headers}: {flow_data}")
                            post_response = requests.post(NETBOX_URL, json=flow_data, headers=headers)
                            if post_response.status_code == 201:
                                logger.debug(f"Flow created: {src_ip} -> {dst_ip}:{service_port}, response: {post_response.text}")
                                new_flows_count += 1
                                conn.execute("""
                                    UPDATE flows
                                    SET written_to_netbox = 1
                                    WHERE src_ip = ? AND dst_ip = ? AND proto = ? AND service_port = ? AND server_id = ? AND timestamp = ?
                                """, (src_ip, dst_ip, proto_name, service_port, server_id, timestamp))
                                conn.commit()
                            elif post_response.status_code == 400 and "unique set" in post_response.text:
                                logger.debug(f"Flow {src_ip}:{service_port} -> {dst_ip} rejected as duplicate by NetBox")
                                conn.execute("""
                                    UPDATE flows
                                    SET written_to_netbox = 1
                                    WHERE src_ip = ? AND dst_ip = ? AND proto = ? AND service_port = ? AND server_id = ? AND timestamp = ?
                                """, (src_ip, dst_ip, proto_name, service_port, server_id, timestamp))
                                conn.commit()
                            else:
                                logger.warning(f"Unexpected POST response for {src_ip} -> {dst_ip}:{service_port}, status: {post_response.status_code}, response: {post_response.text}")
                                if post_response.status_code >= 500:
                                    conn.execute("""
                                        UPDATE flows
                                        SET written_to_netbox = 1
                                        WHERE src_ip = ? AND dst_ip = ? AND proto = ? AND service_port = ? AND server_id = ? AND timestamp = ?
                                    """, (src_ip, dst_ip, proto_name, service_port, server_id, timestamp))
                                    conn.commit()
                    else:
                        logger.warning(f"Check failed for {src_ip} -> {dst_ip}:{service_port}, status: {check_response.status_code}, response: {check_response.text}")

                if new_flows_count > 0:
                    logger.info(f"Successfully sent {new_flows_count} new flows to NetBox")
                else:
                    logger.debug("No new flows created (all checked flows already exist or failed)")
            else:
                logger.debug("No unwritten flows in local DB")
        except Exception as e:
            logger.error(f"Error in send_to_netbox: {e}", exc_info=True)

def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    load_existing_flows()
    threading.Thread(target=send_to_netbox, daemon=True).start()
    logger.info(f"Starting agent on {SERVER_ID}, sniffing on interfaces {', '.join(INTERFACES)}")
    try:
        sniff(iface=INTERFACES, filter=FILTER, prn=process_packet, store=False)
    except Exception as e:
        logger.error(f"Sniffing stopped due to error: {e}", exc_info=True)
    finally:
        logger.info("Agent stopped")

if __name__ == "__main__":
    main()