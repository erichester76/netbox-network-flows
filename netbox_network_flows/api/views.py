from rest_framework import viewsets
from rest_framework.response import Response
from ..models import TrafficFlow
from .serializers import TrafficFlowSerializer

class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer

    def create(self, request, *args, **kwargs):
        # Handle bulk creation from agent submissions
        if isinstance(request.data, dict) and 'flows' in request.data:
            flows = request.data['flows']
            server_id = request.data.get('server_id', '')
            for flow in flows:
                flow['server_id'] = server_id
                serializer = self.get_serializer(data=flow)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({"status": "success"}, status=201)
        return super().create(request, *args, **kwargs)