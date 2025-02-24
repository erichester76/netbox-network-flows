from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm
from .models import TrafficFlow
import logging

class TrafficFlowForm(NetBoxModelForm):
    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'src_content_type', 'dst_content_type', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }

