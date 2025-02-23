from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, BulkEditView, BulkDeleteView, ObjectChangeLogView
from utilities.views import register_model_view, ViewTab
from virtualization.models import VirtualMachine
from dcim.models import Device
from .models import TrafficFlow
from .tables import TrafficFlowTable
from .forms import TrafficFlowForm
from utilities.forms import ConfirmationForm
from django.contrib.contenttypes.models import ContentType
from django.db import models

@register_model_view(VirtualMachine, 'flows', path='flows')
class VirtualMachineFlowsView(ObjectView):
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
        mermaid_code = "graph TD\n"
        nodes = set()
        edges = []
        for flow in flows:
            # Use service_port as dst_port, src_port is assumed ephemeral (0 if not service side)
            src_node = f"{flow.src_ip}:0" if flow.dst_content_type == vm_ct and flow.dst_object_id == instance.pk else f"{flow.src_ip}:{flow.service_port}"
            dst_node = f"{flow.dst_ip}:{flow.service_port}" if flow.dst_content_type == vm_ct and flow.dst_object_id == instance.pk else f"{flow.dst_ip}:0"
            nodes.add(src_node)
            nodes.add(dst_node)
            edges.append(f"{src_node} --> |{flow.protocol}| {dst_node}")
        
        for node in nodes:
            mermaid_code += f"    {node}\n"
        for edge in edges:
            mermaid_code += f"    {edge}\n"
        
        return {
            'flows': flows,
            'mermaid_code': mermaid_code,
        }

@register_model_view(Device, 'flows', path='flows')
class DeviceFlowsView(ObjectView):
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
        mermaid_code = "graph TD\n"
        nodes = set()
        edges = []
        for flow in flows:
            # Use service_port as dst_port, src_port is assumed ephemeral (0 if not service side)
            src_node = f"{flow.src_ip}:0" if flow.dst_content_type == device_ct and flow.dst_object_id == instance.pk else f"{flow.src_ip}:{flow.service_port}"
            dst_node = f"{flow.dst_ip}:{flow.service_port}" if flow.dst_content_type == device_ct and flow.dst_object_id == instance.pk else f"{flow.dst_ip}:0"
            nodes.add(src_node)
            nodes.add(dst_node)
            edges.append(f"{src_node} --> |{flow.protocol}| {dst_node}")
        
        for node in nodes:
            mermaid_code += f"    {node}\n"
        for edge in edges:
            mermaid_code += f"    {edge}\n"
        
        return {
            'flows': flows,
            'mermaid_code': mermaid_code,
        }
        
class TrafficFlowListView(ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable

class TrafficFlowEditView(ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm

class TrafficFlowImportView(ObjectView):
    queryset = TrafficFlow.objects.all()

class TrafficFlowDetailView(ObjectView):
    queryset = TrafficFlow.objects.all()

class TrafficFlowDeleteView(ObjectDeleteView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'plugins:netbox_network_flows:trafficflow_list'
    
class TrafficFlowBulkEditView(BulkEditView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable
    form = TrafficFlowForm
    default_return_url = 'plugins:netbox_network_flows:trafficflow_list'

class TrafficFlowBulkDeleteView(BulkDeleteView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable
    confirmation_form = ConfirmationForm
    default_return_url = 'plugins:netbox_network_flows:trafficflow_list'
    
class TrafficFlowChangelogView(ObjectChangeLogView):
    queryset = TrafficFlow.objects.all()
