from django.shortcuts import get_object_or_404
from netbox.views import generic
from utilities.views import register_model_view
from virtualization.models import VirtualMachine
from .models import TrafficFlow
from .tables import TrafficFlowTable
from .forms import TrafficFlowForm

@register_model_view(VirtualMachine, 'flows', path='flows')
class VirtualMachineFlowsView(generic.ObjectView):
    queryset = VirtualMachine.objects.all()
    template_name = 'netbox_traffic_flows/vm_flows_tab.html'

    tab = {
        'title': 'Traffic Flows',
        'badge': lambda obj: obj.traffic_flows.count(),
        'permission': 'traffic_flows.view_trafficflow'
    }

    def get_extra_context(self, request, instance):
        flows = instance.traffic_flows.all()
        mermaid_code = "graph TD\n"
        nodes = set()
        edges = []
        for flow in flows:
            src_node = f"{flow.src_ip}:{flow.src_port}"
            dst_node = f"{flow.dst_ip}:{flow.dst_port}"
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

class TrafficFlowListView(generic.ObjectListView):
    queryset = TrafficFlow.objects.all()
    table = TrafficFlowTable

class TrafficFlowEditView(generic.ObjectEditView):
    queryset = TrafficFlow.objects.all()
    form = TrafficFlowForm

class TrafficFlowImportView(generic.ObjectView):
    queryset = TrafficFlow.objects.all()

    def get_extra_context(self, request, instance):
        return {}