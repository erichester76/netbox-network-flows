from rest_framework import serializers
from ..models import TrafficFlow, ServiceEndpoint
from django.contrib.contenttypes.models import ContentType

class ServiceEndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEndpoint
        fields = "__all__"
        
class TrafficFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrafficFlow
        fields = "__all__"
        