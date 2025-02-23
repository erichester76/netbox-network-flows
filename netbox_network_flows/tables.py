from .models import TrafficFlow
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables
from django.urls import reverse

class TrafficFlowTable(NetBoxTable):
    src_ip = tables.Column(
        verbose_name='Source IP',
        accessor='src_ip',  # Ensures the raw value is used
        linkify=lambda record: reverse('ipam:ipaddress', kwargs={'pk': record.src_object_id}) if record.src_content_type and record.src_content_type.model == 'ipaddress' else None
    )
    src_object = tables.Column(
        verbose_name='Source Object',
        linkify=True  # Should work for GFKs to VM/Device/IPAddress
    )
    dst_ip = tables.Column(
        verbose_name='Destination IP',
        accessor='dst_ip',
        linkify=lambda record: reverse('ipam:ipaddress', kwargs={'pk': record.dst_object_id}) if record.dst_content_type and record.dst_content_type.model == 'ipaddress' else None
    )
    dst_object = tables.Column(
        verbose_name='Dest Object',
        linkify=True  # Should work for GFKs to VM/Device/IPAddress
    )

    timestamp = columns.DateTimeColumn()

    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('id', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'timestamp')
        default_columns = ('id', 'src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id')