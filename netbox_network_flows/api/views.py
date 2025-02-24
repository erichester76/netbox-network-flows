from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import TrafficFlow, ServiceEndpoint
from .serializers import TrafficFlowSerializer, ServiceEndpointSerializer
from rest_framework.exceptions import ValidationError

class ServiceEndpointViewSet(viewsets.ModelViewSet):
    queryset = ServiceEndpoint.objects.all()
    serializer_class = ServiceEndpointSerializer
    
class TrafficFlowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TrafficFlows to be viewed or edited.
    Supports both single object and bulk creation.
    """
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle both single flow creation and bulk flow creation.
        Single: POST with a single flow object.
        Bulk: POST with a 'flows' key containing a list of flow objects.
        """
        # Check if it's a bulk request
        if isinstance(request.data, dict) and 'flows' in request.data:
            flows = request.data['flows']
            server_id = request.data.get('server_id', '')
            created_flows = []
            for flow in flows:
                flow['server_id'] = server_id  # Override server_id if provided in bulk
                serializer = self.get_serializer(data=flow)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_flows.append(serializer.data)
            return Response(created_flows, status=status.HTTP_201_CREATED)
        
        # Handle single flow creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Ensure service_endpoint is set if provided
        service_endpoint_id = serializer.validated_data.get('service_endpoint')
        if service_endpoint_id:
            try:
                service_endpoint = ServiceEndpoint.objects.get(id=service_endpoint_id)
                serializer.save(service_endpoint=service_endpoint)
            except ServiceEndpoint.DoesNotExist:
                raise ValidationError({"service_endpoint": "Service endpoint does not exist."})
        else:
            serializer.save()