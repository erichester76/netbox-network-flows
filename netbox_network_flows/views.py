from netbox.views.generic import ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView, BulkImportView, BulkEditView, BulkDeleteView, ObjectChangeLogView
from utilities.views import register_model_view, ViewTab
from virtualization.models import VirtualMachine
from .models import TrafficFlow
from .tables import TrafficFlowTable
from .forms import TrafficFlowForm
from utilities.forms import ConfirmationForm

@register_model_view(VirtualMachine, 'flows', path='flows')
class VirtualMachineFlowsView(ObjectView):
    queryset = VirtualMachine.objects.all()
    template_name = 'netbox_network_flows/vm_flows_tab.html'

    tab = ViewTab(
        label='Traffic Flows',
        badge=lambda obj: lambda obj: obj.flows.count() or 0,
    )
 
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
