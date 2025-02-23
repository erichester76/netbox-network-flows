from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

items = (
    PluginMenuItem(
        link='plugins:netbox_network_flows:trafficflow_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:trafficflow_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_flow']
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:trafficflow_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_low']
            ),
        ),
        permissions=['netbox_network_flows.view_flow']
    ),
)

menu = PluginMenu(
    label='Network Flows',
    icon_class='mdi mdi-network',
    groups=(('Flows', items),)
)