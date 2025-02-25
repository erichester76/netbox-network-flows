from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

items = (
    PluginMenuItem(
        link='plugins:netbox_network_flows:trafficflow_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:trafficflow_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:trafficflow_import',
                title='Import',
                icon_class='mdi mdi-upload',
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:netbox_network_flows:serviceendpoint_list',
        link_text='Service Endpoints',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_import',
                title='Import',
                icon_class='mdi mdi-upload',
            ),
        ),
    ),
)

menu = PluginMenu(
    label='Network Flows',
    icon_class='mdi mdi-network',
    groups=(('Flows', items),)
)