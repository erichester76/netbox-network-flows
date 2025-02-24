from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables
from django.urls import reverse

class TrafficFlowTable(NetBoxTable):
    timestamp = columns.DateTimeColumn()
    src_ip = tables.Column(verbose_name='Source IP')
    dst_ip = tables.Column(verbose_name='Destination IP')
    # src_object = tables.Column(verbose_name='Source Object', linkify=True)
    # dst_object = tables.Column(verbose_name='Destination Object', linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('pk', 'id', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'timestamp')
        default_columns = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port')