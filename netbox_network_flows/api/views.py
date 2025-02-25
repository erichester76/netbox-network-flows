from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from netbox_network_flows.models import TrafficFlow, ServiceEndpoint
from .serializers import TrafficFlowSerializer, ServiceEndpointSerializer

class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict) and 'flows' in request.data:
            flows = request.data['flows']
            server_id = request.data.get('server_id', '')
            created_flows = []
            for flow in flows:
                flow['server_id'] = server_id
                serializer = self.get_serializer(data=flow)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_flows.append(serializer.data)
            return Response(created_flows, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        service_endpoint_id = serializer.validated_data.get('service_endpoint')
        if service_endpoint_id:
            try:
                service_endpoint = ServiceEndpoint.objects.get(id=service_endpoint_id)
                serializer.save(service_endpoint=service_endpoint)
            except ServiceEndpoint.DoesNotExist:
                raise ValidationError({"service_endpoint": "Service endpoint does not exist."})
        else:
            serializer.save()

class ServiceEndpointViewSet(viewsets.ModelViewSet):
    queryset = ServiceEndpoint.objects.all()
    serializer_class = ServiceEndpointSerializer