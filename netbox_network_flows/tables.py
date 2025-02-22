import django_tables2 as tables
from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns

class TrafficFlowTable(NetBoxTable):
    src_ip = tables.Column(verbose_name='Source IP')
    dst_ip = tables.Column(verbose_name='Destination IP')
    protocol = tables.Column()
    src_port = tables.Column(verbose_name='Source Port')
    dst_port = tables.Column(verbose_name='Destination Port')
    server_id = tables.Column(verbose_name='Server ID')
    virtual_machine = tables.Column(linkify=True)
    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine', 'timestamp')
        default_columns = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine')