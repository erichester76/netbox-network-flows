from netbox.plugins import PluginConfig, PluginMenuItem, PluginMenu
from django.urls import reverse

class TrafficFlowsConfig(PluginConfig):
    name = 'traffic_flows'
    verbose_name = 'Traffic Flows'
    description = 'Manage network traffic flows between servers'
    version = '0.1'
    author = 'Eric Hester'
    author_email = 'hester1@clemson.edu'
    base_url = 'traffic-flows'
    min_version = '4.1.0'
    max_version = '4.1.99'

config = TrafficFlowsConfig