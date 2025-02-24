from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

items = (

        PluginMenuItem(
        link='plugins:netbox_network_flows:serviceendpoint_list',
        link_text='Flows',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_flow']
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_flow']
            ),
        ),
        permissions=['netbox_network_flows.view_flow']
    ),
        
    PluginMenuItem(
        link='plugins:netbox_network_flows:serviceendpoint_list',
        link_text='Service Endpoints',
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=['netbox_network_flows.add_flow']
            ),
            PluginMenuButton(
                link='plugins:netbox_network_flows:serviceendpoint_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=['netbox_network_flows.add_flow']
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