from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from .models import TrafficFlow
from virtualization.models import VirtualMachine
from dcim.models import Device
from ipam.models import IPAddress
import logging

logger = logging.getLogger(__name__)


class TrafficFlowForm(NetBoxModelForm):
    src_content_type = forms.ChoiceField(
        choices=[],
        required=False,
        label='Source Object Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dst_content_type = forms.ChoiceField(
        choices=[],
        required=False,
        label='Destination Object Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    src_object = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.none(), 
        required=False,
        label='Source Object',
        null_option='None',
        query_params={'content_type_id': '$src_content_type'}
    )
    dst_object = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.none(), 
        required=False,
        label='Destination Object',
        null_option='None',
        query_params={'content_type_id': '$dst_content_type'}
    )

    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'src_content_type', 'dst_content_type', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            
            allowed_models = [VirtualMachine, Device, IPAddress]
            content_types = ContentType.objects.get_for_models(*allowed_models)
            type_choices = [('', '---------')] + [(ct.pk, ct.model_class()._meta.verbose_name.title()) for ct in content_types.values()]
            
            self.fields['src_content_type'].choices = type_choices
            self.fields['dst_content_type'].choices = type_choices

            # Log initial values and querysets
            if self.instance.pk:
                if self.instance.src_content_type:
                    self.initial['src_content_type'] = self.instance.src_content_type.pk
                    self.initial['src_object'] = self.instance.src_object
                    self.fields['src_object'].queryset = self.instance.src_content_type.model_class().objects.all()
                if self.instance.dst_content_type:
                    self.initial['dst_content_type'] = self.instance.dst_content_type.pk
                    self.initial['dst_object'] = self.instance.dst_object
                    self.fields['dst_object'].queryset = self.instance.dst_content_type.model_class().objects.all()


        except Exception as e:
            raise

    def clean(self):
        try:
            cleaned_data = super().clean()
            
            src_content_type_id = cleaned_data.get('src_content_type')
            src_object = cleaned_data.get('src_object')
            if src_content_type_id and src_object:
                self.instance.src_content_type = ContentType.objects.get(pk=src_content_type_id)
                self.instance.src_object_id = src_object.pk
            else:
                self.instance.src_content_type = None
                self.instance.src_object_id = None

            dst_content_type_id = cleaned_data.get('dst_content_type')
            dst_object = cleaned_data.get('dst_object')
            if dst_content_type_id and dst_object:
                self.instance.dst_content_type = ContentType.objects.get(pk=dst_content_type_id)
                self.instance.dst_object_id = dst_object.pk
            else:
                self.instance.dst_content_type = None
                self.instance.dst_object_id = None

            return cleaned_data
        except Exception as e:
            raise