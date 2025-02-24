from netbox.plugins import PluginConfig

class NetworkFlowsConfig(PluginConfig):
    name = 'netbox_network_flows'
    verbose_name = 'Traffic Flows'
    description = 'Manage network traffic flows between servers'
    version = '0.1.1'
    author = 'Eric Hester'
    author_email = 'hester1@clemson.edu'
    base_url = 'flows'
    min_version = '4.1.0'
    max_version = '4.2.99'

config = NetworkFlowsConfig