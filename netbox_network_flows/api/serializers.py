from rest_framework import serializers
from ..models import TrafficFlow
from virtualization.models import VirtualMachine

class TrafficFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlow
        fields = ['id', 'src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine', 'timestamp']