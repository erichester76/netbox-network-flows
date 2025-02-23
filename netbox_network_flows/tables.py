from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables
from django.urls import reverse

class TrafficFlowTable(NetBoxTable):
    src_object = tables.Column(
        verbose_name='Source Object',
        linkify=True  #
    )
    dst_object = tables.Column(
        verbose_name='Dest Object',
        linkify=True  
    )

    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('pk', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'timestamp')
        default_columns = ('pk', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port')