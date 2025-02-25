# netbox_network_flows/navigation.py
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

items = (
    PluginMenuItem(
        link='netbox_network_flows:trafficflow_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='netbox_network_flows:trafficflow_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_flow']
            ),
            PluginMenuButton(
                link='netbox_network_flows:trafficflow_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_flow']
            ),
        ),
        permissions=['netbox_network_flows.view_flow']
    ),
    PluginMenuItem(
        link='netbox_network_flows:serviceendpoint_list',
        link_text='Service Endpoints',
        buttons=(
            PluginMenuButton(
                link='netbox_network_flows:serviceendpoint_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_serviceendpoint']
            ),
            PluginMenuButton(
                link='netbox_network_flows:serviceendpoint_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_serviceendpoint']
            ),
        ),
        permissions=['netbox_network_flows.view_serviceendpoint']
    ),
)

menu = PluginMenu(
    label='Network Flows',
    icon_class='mdi mdi-network',
    groups=(('Flows', items),)
)