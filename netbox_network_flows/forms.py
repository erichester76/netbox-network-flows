from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm, DynamicModelChoiceField
from .models import TrafficFlow
from virtualization.models import VirtualMachine
from dcim.models import Device
from ipam.models import IPAddress

class TrafficFlowForm(NetBoxModelForm):
    # Content type selection fields
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
    
    # Dynamic object selection fields tied to content type
    src_object = DynamicModelChoiceField(
        queryset=None,  # Set dynamically
        required=False,
        label='Source Object',
        null_option='None',
        query_params={
            'content_type_id': '$src_content_type'  # Links to src_content_type field
        }
    )
    dst_object = DynamicModelChoiceField(
        queryset=None,  # Set dynamically
        required=False,
        label='Destination Object',
        null_option='None',
        query_params={
            'content_type_id': '$dst_content_type'  # Links to dst_content_type field
        }
    )

    class Meta:
        model = TrafficFlow
        fields = ('src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'src_content_type', 'src_object', 'dst_content_type', 'dst_object', 'timestamp')
        widgets = {
            'timestamp': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define allowed content types
        allowed_models = [VirtualMachine, Device, IPAddress]
        content_types = ContentType.objects.get_for_models(*allowed_models)
        type_choices = [('', '---------')] + [(ct.pk, ct.model_class()._meta.verbose_name.title()) for ct in content_types.values()]
        
        self.fields['src_content_type'].choices = type_choices
        self.fields['dst_content_type'].choices = type_choices

        # Set initial querysets (filtered dynamically by content_type_id)
        combined_queryset = VirtualMachine.objects.all().union(Device.objects.all(), IPAddress.objects.all())
        self.fields['src_object'].queryset = combined_queryset
        self.fields['dst_object'].queryset = combined_queryset

        # Prepopulate if editing an existing instance
        if self.instance.pk:
            if self.instance.src_content_type:
                self.initial['src_content_type'] = self.instance.src_content_type.pk
                self.initial['src_object'] = self.instance.src_object
            if self.instance.dst_content_type:
                self.initial['dst_content_type'] = self.instance.dst_content_type.pk
                self.initial['dst_object'] = self.instance.dst_object

    def clean(self):
        cleaned_data = super().clean()
        
        # Handle src_content_type and src_object
        src_content_type_id = cleaned_data.get('src_content_type')
        src_object = cleaned_data.get('src_object')
        if src_content_type_id and src_object:
            self.instance.src_content_type = ContentType.objects.get(pk=src_content_type_id)
            self.instance.src_object_id = src_object.pk
        else:
            self.instance.src_content_type = None
            self.instance.src_object_id = None

        # Handle dst_content_type and dst_object
        dst_content_type_id = cleaned_data.get('dst_content_type')
        dst_object = cleaned_data.get('dst_object')
        if dst_content_type_id and dst_object:
            self.instance.dst_content_type = ContentType.objects.get(pk=dst_content_type_id)
            self.instance.dst_object_id = dst_object.pk
        else:
            self.instance.dst_content_type = None
            self.instance.dst_object_id = None

        return cleaned_data