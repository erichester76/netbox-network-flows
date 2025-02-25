from rest_framework import serializers
from netbox_network_flows.models import TrafficFlow, ServiceEndpoint
from django.contrib.contenttypes.models import ContentType

class ServiceEndpointSerializer(serializers.ModelSerializer):
    flow_count = serializers.IntegerField(read_only=True)
    flow_link = serializers.SerializerMethodField()

    class Meta:
        model = ServiceEndpoint
        fields = ['id', 'application_name', 'service_port', 'process_name', 'flow_count', 'flow_link']

    def get_flow_link(self, obj):
        return f"/netbox/api/plugins/flows/flows/?service_endpoint={obj.id}"
    
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