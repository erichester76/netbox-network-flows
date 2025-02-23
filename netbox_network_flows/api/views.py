from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import TrafficFlow
from serializers import TrafficFlowSerializer

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
                serializer.save()
                created_flows.append(serializer.data)
            return Response(created_flows, status=status.HTTP_201_CREATED)
        
        # Handle single flow creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)