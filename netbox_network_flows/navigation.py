from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

items = (
    PluginMenuItem(
        link='plugins:traffic_flows:flow_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='plugins:traffic_flows:flow_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color='green',
                permissions=['traffic_flows.add_trafficflow']
            ),
            PluginMenuButton(
                link='plugins:traffic_flows:flow_import',
                title='Import',
                icon_class='mdi mdi-upload',
                color='blue',
                permissions=['traffic_flows.add_trafficflow']
            ),
        ),
        permissions=['traffic_flows.view_trafficflow']
    ),
)

menu = PluginMenu(
    label='Network Flows',
    icon_class='mdi mdi-network',
    groups=(('Flows', items),)
)