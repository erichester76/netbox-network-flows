from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import TrafficFlow
from .serializers import TrafficFlowSerializer

class TrafficFlowViewSet(viewsets.ModelViewSet):

    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer

    def create(self, request, *args, **kwargs):
  
        # Check if it's a bulk request
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
            return Response(created_flows, status=status.HTTP_201_CREATED)
        
        # Handle single flow creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)