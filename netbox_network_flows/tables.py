from django import forms
from .models import TrafficFlow
from netbox.forms import NetBoxModelForm
from virtualization.models import VirtualMachine

class TrafficFlowForm(NetBoxModelForm):
    virtual_machine = forms.ModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label='Virtual Machine'
    )

    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id', 'virtual_machine', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }