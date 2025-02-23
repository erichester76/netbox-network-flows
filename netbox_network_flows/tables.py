import django_tables2 as tables
from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns

class TrafficFlowTable(NetBoxTable):
    virtual_machine = tables.Column(linkify=True)
    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine', 'timestamp')
        default_columns = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine')