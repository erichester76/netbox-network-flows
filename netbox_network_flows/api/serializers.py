from rest_framework import serializers
from ..models import TrafficFlow
from django.contrib.contenttypes.models import ContentType

class TrafficFlowSerializer(serializers.ModelSerializer):
    src_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), allow_null=True, default=None)
    dst_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), allow_null=True, default=None)

    class Meta:
        model = TrafficFlow
        fields = ['id', 'src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'src_content_type', 'src_object_id', 'dst_content_type', 'dst_object_id', 'timestamp']