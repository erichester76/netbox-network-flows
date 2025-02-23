import django_tables2 as tables
from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns

class TrafficFlowTable(NetBoxTable):
    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'timestamp')
        default_columns = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id')