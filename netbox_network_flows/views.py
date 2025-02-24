from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from virtualization.models import VirtualMachine
from dcim.models import Device
from .models import TrafficFlow
from .tables import TrafficFlowTable
from .forms import TrafficFlowForm
from utilities.forms import ConfirmationForm
from django.contrib.contenttypes.models import ContentType
from django.db import models
import json

class TrafficFlowListView(generic.ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable
    template_name = 'netbox_network_flows/flow_list.html'
    actions = {
        'add': {'add': True},
        'edit': {'change': True},
        'delete': {'delete': True},
        'import': {'add': True}
    }

class TrafficFlowEditView(generic.ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm
    template_name = 'netbox_network_flows/flow_edit.html'

class TrafficFlowDeleteView(generic.ObjectDeleteView):
    queryset = TrafficFlow.objects.all()
    template_name = 'netbox_network_flows/flow_delete.html'
    default_return_url = 'netbox_network_flows:flow_list'

class TrafficFlowImportView(generic.ObjectView):
    queryset = TrafficFlow.objects.all()
    template_name = 'netbox_network_flows/flow_import.html'

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

        # Prepare data for vis.js
        nodes = set()
        edges = []
        for flow in flows:
            src_name = str(flow.src_object) if flow.src_object else flow.src_ip
            dst_name = str(flow.dst_object) if flow.dst_object else flow.dst_ip
            src_id = f"{flow.src_content_type_id}_{flow.src_object_id}" if flow.src_object else flow.src_ip
            dst_id = f"{flow.dst_content_type_id}_{flow.dst_object_id}" if flow.dst_object else flow.dst_ip
            nodes.add((src_id, src_name))
            nodes.add((dst_id, dst_name))
            edges.append({
                'from': src_id,
                'to': dst_id,
                'label': f"{flow.protocol}:{flow.service_port}",
                'color': {'color': 'blue' if flow.protocol == 'tcp' else 'red'}
            })

        vis_data = {
            'nodes': [{'id': nid, 'label': nlabel} for nid, nlabel in nodes],
            'edges': edges
        }

        return {
            'flows_table': flows_table,
            'vis_data': json.dumps(vis_data),
        }

# Similar changes for DeviceFlowsView...
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
        ).prefetch_related('src_content_type', 'dst_content_type')
        flows_table = TrafficFlowTable(flows)
        flows_table.configure(request)

        nodes = set()
        edges = []
        for flow in flows:
            src_name = str(flow.src_object) if flow.src_object else flow.src_ip
            dst_name = str(flow.dst_object) if flow.dst_object else flow.dst_ip
            src_id = f"{flow.src_content_type_id}_{flow.src_object_id}" if flow.src_object else flow.src_ip
            dst_id = f"{flow.dst_content_type_id}_{flow.dst_object_id}" if flow.dst_object else flow.dst_ip
            nodes.add((src_id, src_name))
            nodes.add((dst_id, dst_name))
            edges.append({
                'from': src_id,
                'to': dst_id,
                'label': f"{flow.protocol}:{flow.service_port}",
                'color': {'color': 'blue' if flow.protocol == 'tcp' else 'red'}
            })

        vis_data = {
            'nodes': [{'id': nid, 'label': nlabel} for nid, nlabel in nodes],
            'edges': edges
        }

        return {
            'flows_table': flows_table,
            'vis_data': json.dumps(vis_data),
        }

