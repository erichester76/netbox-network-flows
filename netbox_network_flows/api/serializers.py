from rest_framework import serializers
from netbox_network_flows.models import TrafficFlow, ServiceEndpoint
from django.contrib.contenttypes.models import ContentType

class ServiceEndpointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEndpoint
        fields = ['id', 'application_name', 'service_port', 'process_name']

class TrafficFlowSerializer(serializers.ModelSerializer):
    src_content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        allow_null=True,
        default=None
    )
    dst_content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        allow_null=True,
        default=None
    )
    service_endpoint = serializers.PrimaryKeyRelatedField(
        queryset=ServiceEndpoint.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = TrafficFlow
        fields = [
            'id', 'src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id',
            'src_content_type', 'src_object_id', 'dst_content_type', 'dst_object_id',
            'timestamp', 'service_endpoint'
        ]