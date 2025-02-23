from django import forms
from netbox.forms import NetBoxModelForm
from netbox_network_flows.models import TrafficFlow

class TrafficFlowForm(NetBoxModelForm):
    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }