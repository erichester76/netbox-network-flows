from rest_framework import serializers
from ..models import TrafficFlow, ServiceEndpoint
from django.contrib.contenttypes.models import ContentType

class ServiceEndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEndpoint
        fields = "__all__"
        
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
        fields = "__all__"