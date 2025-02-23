from django.urls import path
from .views import TrafficFlowListView, TrafficFlowEditView, TrafficFlowImportView, TrafficFlowBulkEditView, TrafficFlowBulkDeleteView, TrafficFlowChangelogView
from .models import TrafficFlow

urlpatterns = [
    path('flows/', TrafficFlowListView.as_view(), name='trafficflow_list'),
    path('flows/add/', TrafficFlowEditView.as_view(), name='trafficflow_add'),
    path('flows/<int:pk>/edit/', TrafficFlowEditView.as_view(), name='trafficflow_edit'),
    path('flows/<int:pk>/delete/', TrafficFlowEditView.as_view(), name='trafficflow_delete'),
    path('flows/bulk/import/', TrafficFlowImportView.as_view(), name='trafficflow_import'),
    path('flows/bulk/edit/', TrafficFlowBulkEditView.as_view(), name='trafficflow_bulk_edit'),
    path('flows/bulk/delete/', TrafficFlowBulkDeleteView.as_view(), name='trafficflow_bulk_delete'),    
    path('flows/<int:pk>/changelog/', TrafficFlowChangelogView.as_view(), name='trafficflow_changelog', kwargs={'model': TrafficFlow})
]