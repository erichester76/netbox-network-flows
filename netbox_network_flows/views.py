from .models import TrafficFlow
from .tables import TrafficFlowTable
from .forms import TrafficFlowForm
from django.contrib.contenttypes.models import ContentType
from django.db import models
from utilities.views import register_model_view, ViewTab
from netbox.views import generic
from virtualization.models import VirtualMachine
from dcim.models import Device

class TrafficFlowListView(generic.ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable
    actions = {
        'add': {'add': True},
        'edit': {'change': True},
        'delete': {'delete': True},
        'import': {'add': True}
    }

class TrafficFlowEditView(generic.ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowDeleteView(generic.ObjectDeleteView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowImportView(generic.BulkImportView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowBulkEditView(generic.BulkEditView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowBulkDeleteView(generic.BulkDeleteView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'netbox_network_flows:flow_list'
    
class TrafficFlowChangelogView(generic.ObjectChangeLogView):
    queryset = TrafficFlow.objects.all()
    
@register_model_view(VirtualMachine, 'flows', path='flows')
class VirtualMachineFlowsView(generic.ObjectView):
    queryset = VirtualMachine.objects.all()
    template_name = 'netbox_network_flows/vm_flows_tab.html'

    tab = ViewTab(
        label='Traffic Flows',
        badge=lambda obj: TrafficFlow.objects.filter(
            models.Q(src_content_type=ContentType.objects.get_for_model(VirtualMachine), src_object_id=obj.pk) |
            models.Q(dst_content_type=ContentType.objects.get_for_model(VirtualMachine), dst_object_id=obj.pk)
        ).count() or 0,
    )
 
    def get_extra_context(self, request, instance):
        vm_ct = ContentType.objects.get_for_model(VirtualMachine)
        flows = TrafficFlow.objects.filter(
            models.Q(src_content_type=vm_ct, src_object_id=instance.pk) |
            models.Q(dst_content_type=vm_ct, dst_object_id=instance.pk)
        )
        flows_table = TrafficFlowTable(flows)
        flows_table.configure(request)
        return {
            'flows_table': flows_table,
        }

@register_model_view(Device, 'flows', path='flows')
class DeviceFlowsView(generic.ObjectView):
    queryset = Device.objects.all()
    template_name = 'netbox_network_flows/device_flows_tab.html'

    tab = ViewTab(
        label='Traffic Flows',
        badge=lambda obj: TrafficFlow.objects.filter(
            models.Q(src_content_type=ContentType.objects.get_for_model(Device), src_object_id=obj.pk) |
            models.Q(dst_content_type=ContentType.objects.get_for_model(Device), dst_object_id=obj.pk)
        ).count() or 0,
    )
 
    def get_extra_context(self, request, instance):
        device_ct = ContentType.objects.get_for_model(Device)
        flows = TrafficFlow.objects.filter(
            models.Q(src_content_type=device_ct, src_object_id=instance.pk) |
            models.Q(dst_content_type=device_ct, dst_object_id=instance.pk)
        )
        flows_table = TrafficFlowTable(flows)
        flows_table.configure(request)
        return {
            'flows_table': flows_table,
        }