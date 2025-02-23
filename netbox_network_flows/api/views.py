from rest_framework import viewsets
from rest_framework.response import Response
from traffic_flows.models import TrafficFlow
from traffic_flows.api.serializers import TrafficFlowSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'server_id']

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict) and 'flows' in request.data:
            flows = request.data['flows']
            server_id = request.data.get('server_id', '')
            created_flows = []
            for flow in flows:
                flow['server_id'] = server_id
                serializer = self.get_serializer(data=flow)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                created_flows.append(serializer.data)
            return Response(created_flows, status=201)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)