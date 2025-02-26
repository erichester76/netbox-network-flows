from scapy.all import sniff, IP, TCP, UDP
import time
import socket
import os
import netifaces
import ipaddress
import requests
import logging
import psutil
from collections import defaultdict

# Configuration
NETBOX_BASE_URL = "https://o11y.app.clemson.edu/netbox/api/plugins/flows/"
NETBOX_TOKEN = "25c89f4320476edf29a6cb24a1d2b085b1fd5264"

EPHEMERAL_PORT_MIN = 10000
SERVICE_PORT_THRESHOLD = 4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]  # Console-only logging, no logfile
)
logger = logging.getLogger(__name__)

SERVER_ID = socket.gethostname().split('.')[0]
logger.info(f"Starting agent on {SERVER_ID}")

# In-memory caches for NetBox data
traffic_flow_cache = {}  # Cache for TrafficFlow: (src_ip, dst_ip, protocol, service_port, server_id) -> flow_id
service_endpoint_cache = {}  # Cache for ServiceEndpoint: service_port -> (endpoint_id, process_name, application_name)

def get_local_interfaces_and_ips():
    interfaces = []
    local_ips = set()
    physical_ip = None
    for iface in netifaces.interfaces():
        if iface == "lo" or iface.startswith(('docker', 'br-', 'veth', 'virbr')):
            continue
        if not iface.startswith('e'):
            continue
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr["addr"]
                netmask = addr["netmask"]
                try:
                    network = ipaddress.ip_network(f"{ip}/{netmask}", strict=False)
                    interfaces.append(iface)
                    local_ips.add(ip)
                    if not physical_ip:
                        physical_ip = ip
                except ValueError:
                    continue
    interfaces.append('lo')  # Include localhost
    return interfaces, local_ips, physical_ip

INTERFACES, LOCAL_IPS, PHYSICAL_IP = get_local_interfaces_and_ips()
if not INTERFACES:
    logger.error("No valid network interfaces found. Exiting.")
    exit(1)
if not PHYSICAL_IP:
    logger.error("No physical IP found for substitution. Exiting.")
    exit(1)

FILTER = " or ".join(f"net {subnet}" for subnet in [str(ipaddress.ip_network(f"{ip}/24", strict=False)) for ip in LOCAL_IPS]) + " or net 127.0.0.0/8"
logger.info(f"Constructed filter: {FILTER}")

port_connections = defaultdict(lambda: {'src_ports': set(), 'dst_ports': set()})

def get_process_name(port):
    """Get the process name listening on a given port using psutil, with logging."""
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                try:
                    process = psutil.Process(conn.pid)
                    process_name = process.name()
                    logger.info(f"Retrieved process name '{process_name}' for port {port}")
                    return process_name
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return None
        return None
    except Exception as e:
        logger.error(f"Error getting process for port {port}: {e}")
        return None

def check_existing_traffic_flow(src_ip, dst_ip, protocol, service_port, server_id):
    """Check if a TrafficFlow exists in NetBox or cache, returning its ID if found."""
    key = (src_ip, dst_ip, protocol, service_port, server_id)
    if key in traffic_flow_cache:
        return traffic_flow_cache[key]

    headers = {"Authorization": f"Token {NETBOX_TOKEN}", "Content-Type": "application/json"}
    flow_url = NETBOX_BASE_URL + "flows/"
    params = {
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'protocol': protocol,
        'service_port': service_port,
        'server_id': server_id
    }
    try:
        response = requests.get(flow_url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()['results']
            if results:
                flow_id = results[0]['id']
                traffic_flow_cache[key] = flow_id
                logger.info(f"Found existing TrafficFlow ID {flow_id} for {src_ip} -> {dst_ip}:{service_port}")
                return flow_id
    except requests.RequestException as e:
        logger.error(f"Failed to check existing TrafficFlow: {e}")
    return None

def check_existing_service_endpoint(service_port):
    """Check if a ServiceEndpoint exists in NetBox or cache, returning its data if found."""
    if service_port in service_endpoint_cache:
        endpoint_id, cached_process_name, cached_application_name = service_endpoint_cache[service_port]
        return endpoint_id, cached_process_name, cached_application_name

    headers = {"Authorization": f"Token {NETBOX_TOKEN}", "Content-Type": "application/json"}
    endpoint_url = NETBOX_BASE_URL + "service-endpoints/"
    params = {'service_port': service_port}
    try:
        response = requests.get(endpoint_url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()['results']
            # Filter the results to find the exact match by service_port
            matching_endpoint = next((item for item in results if item['service_port'] == service_port), None)
            if matching_endpoint:
                endpoint_id = matching_endpoint['id']
                process_name = matching_endpoint.get('process_name', None)
                application_name = matching_endpoint.get('application_name', f"generic_{service_port}")
                service_endpoint_cache[service_port] = (endpoint_id, process_name, application_name)
                logger.info(f"Found existing ServiceEndpoint ID {endpoint_id} for port {service_port} (process_name: {process_name}, application_name: {application_name})")
                return endpoint_id, process_name, application_name
    except requests.RequestException as e:
        logger.error(f"Failed to check existing ServiceEndpoint: {e}")
    return None, None, None

def update_service_endpoint(endpoint_id, service_port, process_name):
    """Update an existing ServiceEndpoint with new process_name and application_name."""
    headers = {"Authorization": f"Token {NETBOX_TOKEN}", "Content-Type": "application/json"}
    endpoint_url = f"{NETBOX_BASE_URL}service-endpoints/{endpoint_id}/"
    update_data = {
        "application_name": f"{process_name or 'generic'}_{service_port}",
        "process_name": process_name or 'generic'
    }
    try:
        response = requests.patch(endpoint_url, json=update_data, headers=headers)
        response.raise_for_status()
        logger.info(f"Updated ServiceEndpoint ID {endpoint_id} for port {service_port} with process_name '{process_name}' and application_name '{update_data['application_name']}'")
        # Update cache with new values
        service_endpoint_cache[service_port] = (endpoint_id, process_name, update_data['application_name'])
    except requests.RequestException as e:
        logger.error(f"Failed to update ServiceEndpoint ID {endpoint_id}: {e}")

def process_packet(packet):
    try:
        if IP not in packet:
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
            return

        # Replace 127.0.0.1 with physical IP for lo0 flows
        if src_ip == "127.0.0.1":
            src_ip = PHYSICAL_IP
        if dst_ip == "127.0.0.1":
            dst_ip = PHYSICAL_IP

        # Track connections
        port_connections[(dst_ip, dst_port)]['src_ports'].add(src_port)
        port_connections[(src_ip, src_port)]['dst_ports'].add(dst_port)

        # Determine service port and identify local IP with service port
        store_src_ip = src_ip
        store_dst_ip = dst_ip
        service_port = None
        local_ip_with_service = None

        if len(port_connections[(dst_ip, dst_port)]['src_ports']) >= SERVICE_PORT_THRESHOLD:
            service_port = dst_port
            if dst_ip in LOCAL_IPS:
                local_ip_with_service = dst_ip
        elif len(port_connections[(src_ip, src_port)]['dst_ports']) >= SERVICE_PORT_THRESHOLD:
            store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
            store_dst_ip = src_ip
            service_port = src_port
            if src_ip in LOCAL_IPS:
                local_ip_with_service = src_ip
        elif src_port < EPHEMERAL_PORT_MIN and dst_port < EPHEMERAL_PORT_MIN:
            if src_port < dst_port:
                store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
                store_dst_ip = src_ip
                service_port = src_port
                if src_ip in LOCAL_IPS:
                    local_ip_with_service = src_ip
            else:
                service_port = dst_port
                if dst_ip in LOCAL_IPS:
                    local_ip_with_service = dst_ip
        elif dst_port < EPHEMERAL_PORT_MIN:
            service_port = dst_port
            if dst_ip in LOCAL_IPS:
                local_ip_with_service = dst_ip
        elif src_port < EPHEMERAL_PORT_MIN:
            store_src_ip = dst_ip  # Flip IPs so src_port becomes dst_port
            store_dst_ip = src_ip
            service_port = src_port
            if src_ip in LOCAL_IPS:
                local_ip_with_service = src_ip
        else:
            return

        if service_port is None:
            return


        # Check for existing TrafficFlow before creating
        flow_id = check_existing_traffic_flow(store_src_ip, store_dst_ip, proto_name, service_port, SERVER_ID)
        if flow_id:
            return

        # Send TrafficFlow to NetBox for all flows
        headers = {"Authorization": f"Token {NETBOX_TOKEN}", "Content-Type": "application/json"}
        flow_url = NETBOX_BASE_URL + "flows/"
        flow_data = {
            "src_ip": store_src_ip,
            "dst_ip": store_dst_ip,
            "protocol": proto_name,
            "service_port": service_port,
            "server_id": SERVER_ID,
            "service_endpoint": None  # Default to None for non-local flows
        }

        try:
            flow_response = requests.post(flow_url, json=flow_data, headers=headers)
            flow_response.raise_for_status()
            flow_id = flow_response.json()['id']
            traffic_flow_cache[(store_src_ip, store_dst_ip, proto_name, service_port, SERVER_ID)] = flow_id
            logger.info(f"Created TrafficFlow ID {flow_id} for {store_src_ip} -> {store_dst_ip}:{service_port}")
        except requests.RequestException as e:
            logger.error(f"Failed to create TrafficFlow: {e}")
            return

        # Create or update ServiceEndpoint if a local IP has the service port
        if local_ip_with_service and service_port is not None and service_port < EPHEMERAL_PORT_MIN:
            process_name = get_process_name(service_port)
            service_endpoint_data = {
                "application_name": f"{process_name or 'generic'}_{service_port}",
                "service_port": service_port,
                "process_name": process_name or 'generic'
            }

            endpoint_url = NETBOX_BASE_URL + "service-endpoints/"
            service_endpoint_id, existing_process_name, existing_application_name = check_existing_service_endpoint(service_port)
            if service_endpoint_id:
                logger.info(f"Found existing ServiceEndpoint ID {service_endpoint_id} for port {service_port} (current process_name: {existing_process_name}, current application_name: {existing_application_name})")
                # Check if process_name needs updating
                if process_name and (existing_process_name != process_name or existing_application_name != f"{process_name or 'generic'}_{service_port}"):
                    update_service_endpoint(service_endpoint_id, service_port, process_name)
                logger.info(f"Using cached/existing ServiceEndpoint ID {service_endpoint_id} for port {service_port}")
            else:
                try:
                    logger.info(f"Creating new ServiceEndpoint for port {service_port}")
                    endpoint_response = requests.post(endpoint_url, json=service_endpoint_data, headers=headers)
                    endpoint_response.raise_for_status()
                    service_endpoint_id = endpoint_response.json()['id']
                    service_endpoint_cache[service_port] = (service_endpoint_id, process_name, f"{process_name or 'generic'}_{service_port}")
                    logger.info(f"Created new ServiceEndpoint ID {service_endpoint_id} for port {service_port} (process_name: {process_name}")
                except requests.RequestException as e:
                    logger.error(f"Failed to create ServiceEndpoint: {e}")
                    return

            # Update TrafficFlow with ServiceEndpoint ID
            flow_update_data = {
                "service_endpoint": int(service_endpoint_id)
            }
            try:
                flow_update_response = requests.patch(f"{flow_url}{flow_id}/", json=flow_update_data, headers=headers)
                flow_update_response.raise_for_status()
                logger.info(f"Updated TrafficFlow ID {flow_id} with ServiceEndpoint ID {service_endpoint_id} for port {service_port}")
            except requests.RequestException as e:
                logger.error(f"Failed to update TrafficFlow with ServiceEndpoint: {e}")

    except Exception as e:
        logger.error(f"Error processing packet: {e}")

def main():
    logger.info(f"Starting agent on {SERVER_ID}, sniffing on interfaces {', '.join(INTERFACES)}")
    try:
        sniff(iface=INTERFACES, filter=FILTER, prn=process_packet, store=False)
    except Exception as e:
        logger.error(f"Sniffing stopped due to error: {e}")
    finally:
        logger.info("Agent stopped")

if __name__ == "__main__":
    main()