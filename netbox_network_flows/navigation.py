from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

items = (
    PluginMenuItem(
        link='plugins:netbox_network_flows:flow_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:flow_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_trafficflow']
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:flow_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_trafficflow']
            ),
        ),
        permissions=['netbox_network_flows.view_trafficflow']
    ),
)

menu = PluginMenu(
    label='Network Flows',
    icon_class='mdi mdi-network',
    groups=(('Flows', items),)
)