from django.shortcuts import get_object_or_404
from netbox.views import generic
from netbox.registry import register_model_view
from netbox.views.generic.base import ViewTab
from virtualization.models import VirtualMachine
from dcim.models import Device
from netbox_network_flows.models import TrafficFlow
from netbox_network_flows.tables import TrafficFlowTable
from netbox_network_flows.forms import TrafficFlowForm
from django.contrib.contenttypes.models import ContentType
from django.db import models
from collections import defaultdict  # Added import

class TrafficFlowListView(generic.ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable

class TrafficFlowEditView(generic.ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm

class TrafficFlowDeleteView(generic.ObjectDeleteView):
    queryset = TrafficFlow.objects.all()
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowImportView(generic.ObjectView):
    queryset = TrafficFlow.objects.all()

    def get_extra_context(self, request, instance):
        return {}

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

        mermaid_code = "graph TD\n"
        nodes = set()
        edges = []
        # Group flows by src_content_type and src_object_id
        src_groups = defaultdict(list)
        for flow in flows:
            group_key = f"{flow.src_content_type_id}_{flow.src_object_id}" if flow.src_content_type_id and flow.src_object_id else "unassigned"
            src_groups[group_key].append(flow)

        for group_key, group_flows in src_groups.items():
            group_label = group_key if group_key == "unassigned" else f"{group_flows[0].src_object}"
            mermaid_code += f"    subgraph {group_label.replace(' ', '_').replace('.', '_')}\n"
            for flow in group_flows:
                src_name = str(flow.src_object) if flow.src_object else f"{flow.src_ip}"
                dst_name = str(flow.dst_object) if flow.dst_object else f"{flow.dst_ip}"
                src_node = f"{src_name}:0" if flow.dst_content_type == vm_ct and flow.dst_object_id == instance.pk else f"{src_name}:{flow.service_port}"
                dst_node = f"{dst_name}:{flow.service_port}" if flow.dst_content_type == vm_ct and flow.dst_object_id == instance.pk else f"{dst_name}:0"
                edge = f"{src_node} --> |{flow.protocol}| {dst_node}"
                src_node = src_node.replace(" ", "_").replace(".", "_").replace(":", "_")
                dst_node = dst_node.replace(" ", "_").replace(".", "_").replace(":", "_")
                edge = edge.replace(" ", "_").replace(".", "_").replace(":", "_")
                nodes.add(src_node)
                nodes.add(dst_node)
                edges.append(edge)
            mermaid_code += "    end\n"

        for node in nodes:
            mermaid_code += f"    {node}\n"
        for edge in edges:
            mermaid_code += f"    {edge}\n"
        
        return {
            'flows_table': flows_table,
            'mermaid_code': mermaid_code,
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

        mermaid_code = "graph TD\n"
        nodes = set()
        edges = []
        # Group flows by src_content_type and src_object_id
        src_groups = defaultdict(list)
        for flow in flows:
            group_key = f"{flow.src_content_type_id}_{flow.src_object_id}" if flow.src_content_type_id and flow.src_object_id else "unassigned"
            src_groups[group_key].append(flow)

        for group_key, group_flows in src_groups.items():
            group_label = group_key if group_key == "unassigned" else f"{group_flows[0].src_object}"
            mermaid_code += f"    subgraph {group_label.replace(' ', '_').replace('.', '_')}\n"
            for flow in group_flows:
                src_name = str(flow.src_object) if flow.src_object else f"{flow.src_ip}"
                dst_name = str(flow.dst_object) if flow.dst_object else f"{flow.dst_ip}"
                src_node = f"{src_name}:0" if flow.dst_content_type == device_ct and flow.dst_object_id == instance.pk else f"{src_name}:{flow.service_port}"
                dst_node = f"{dst_name}:{flow.service_port}" if flow.dst_content_type == device_ct and flow.dst_object_id == instance.pk else f"{dst_name}:0"
                edge = f"{src_node} --> |{flow.protocol}| {dst_node}"
                src_node = src_node.replace(" ", "_").replace(".", "_").replace(":", "_")
                dst_node = dst_node.replace(" ", "_").replace(".", "_").replace(":", "_")
                edge = edge.replace(" ", "_").replace(".", "_").replace(":", "_")
                nodes.add(src_node)
                nodes.add(dst_node)
                edges.append(edge)
            mermaid_code += "    end\n"

        for node in nodes:
            mermaid_code += f"    {node}\n"
        for edge in edges:
            mermaid_code += f"    {edge}\n"
        
        return {
            'flows_table': flows_table,
            'mermaid_code': mermaid_code,
        }