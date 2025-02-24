import django_tables2 as tables
from netbox_network_flows.models import TrafficFlow
from netbox.tables import NetBoxTable, columns
from django.urls import reverse

class TrafficFlowTable(NetBoxTable):
    id = tables.Column(
        verbose_name='ID',
        linkify=lambda record: reverse('netbox_network_flows:flow_edit', kwargs={'pk': record.pk})
    )
    src_ip = tables.Column(verbose_name='Source IP')
    src_object = tables.Column(verbose_name='Source Object', linkify=True)
    dst_ip = tables.Column(verbose_name='Destination IP')
    dst_object = tables.Column(verbose_name='Dest Object', linkify=True)
    protocol = tables.Column()
    service_port = tables.Column(verbose_name='Service Port')
    server_id = tables.Column(verbose_name='Server ID')
    timestamp = columns.DateTimeColumn()
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('id', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'timestamp', 'actions')
        default_columns = ('id', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port')