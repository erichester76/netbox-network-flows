from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from virtualization.models import VirtualMachine
from dcim.models import Device
from .models import TrafficFlow, ServiceEndpoint
from .tables import TrafficFlowTable, ServiceEndpointTable
from .forms import TrafficFlowForm, ServiceEndpointForm
from .filtersets import ServiceEndpointFilterSet, TrafficFlowFilterSet
from django.contrib.contenttypes.models import ContentType
from django.db import models
import json

class ServiceEndpointListView(generic.ObjectListView):
    queryset = ServiceEndpoint.objects.all()
    table = ServiceEndpointTable
    #filterset = ServiceEndpointFilterSet

class ServiceEndpointEditView(generic.ObjectEditView):
    queryset = ServiceEndpoint.objects.all()
    form = ServiceEndpointForm
    default_return_url = 'plugins:netbox_network_flows:serviceendpoint_list'

class ServiceEndpointDeleteView(generic.ObjectDeleteView):
    queryset = ServiceEndpoint.objects.all()
    default_return_url = 'plugins:netbox_network_flows:serviceendpoint_list'

class ServiceEndpointBulkEditView(generic.BulkEditView):
    queryset = ServiceEndpoint.objects.all()
    default_return_url = 'plugins:netbox_network_flows:serviceendpoint_list'

class ServiceEndpointBulkDeleteView(generic.BulkDeleteView):
    queryset = ServiceEndpoint.objects.all()
    default_return_url = 'plugins:netbox_network_flows:serviceendpoint_list'

class ServiceEndpointImportView(generic.BulkImportView):
    queryset = ServiceEndpoint.objects.all()

class ServiceEndpointChangelogView(generic.ObjectChangeLogView):
    queryset = ServiceEndpoint.objects.all()

class TrafficFlowListView(generic.ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable
    #filterset = TrafficFlowFilterSet

class TrafficFlowEditView(generic.ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm

class TrafficFlowDeleteView(generic.ObjectDeleteView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'plugins:netbox_network_flows:flow_list'

class TrafficFlowImportView(generic.BulkImportView):
    queryset = TrafficFlow.objects.all()

class TrafficFlowBulkEditView(generic.BulkEditView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'plugins:netbox_network_flows:flow_list'

class TrafficFlowBulkDeleteView(generic.BulkDeleteView):
    queryset = TrafficFlow.objects.all()

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
        ).prefetch_related('src_content_type', 'dst_content_type')
        flows_table = TrafficFlowTable(flows)
        flows_table.configure(request)

        return {
            'flows_table': flows_table,
        }

# Apply similar changes to DeviceFlowsView
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
        vm_ct = ContentType.objects.get_for_model(Device)
        flows = TrafficFlow.objects.filter(
            models.Q(src_content_type=vm_ct, src_object_id=instance.pk) |
            models.Q(dst_content_type=vm_ct, dst_object_id=instance.pk)
        ).prefetch_related('src_content_type', 'dst_content_type')
        flows_table = TrafficFlowTable(flows)
        flows_table.configure(request)

      
        return {
            'flows_table': flows_table,
        }