from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables
from django.urls import reverse

class TrafficFlowTable(NetBoxTable):
    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'timestamp')
        default_columns = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port')