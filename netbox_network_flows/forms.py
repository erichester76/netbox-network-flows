from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm
from .models import TrafficFlow, ServiceEndpoint



class ServiceEndpointForm(NetBoxModelForm):
    class Meta:
        model = ServiceEndpoint
        fields = ('application_name', 'service_port', 'process_name')
        widgets = {
            'service_port': forms.NumberInput(attrs={'step': '1'}),
        }
        
class TrafficFlowForm(NetBoxModelForm):
    
    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'src_content_type', 'dst_content_type', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }

   