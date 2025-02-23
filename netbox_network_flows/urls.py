from django.urls import path, include
from .views import TrafficFlowListView, TrafficFlowEditView, TrafficFlowImportView, TrafficFlowBulkEditView, TrafficFlowBulkDeleteView


urlpatterns = [
    path('flows/', TrafficFlowListView.as_view(), name='trafficflow_list'),
    path('flows/add/', TrafficFlowEditView.as_view(), name='trafficflow_add'),
    path('flows/<int:pk>/edit/', TrafficFlowEditView.as_view(), name='trafficflow_edit'),
    path('flows/<int:pk>/delete/', TrafficFlowEditView.as_view(), name='trafficflow_delete'),
    path('flows/bulk/import/', TrafficFlowImportView.as_view(), name='trafficflow_bulk_import'),
    path('flows/bulk/edit/', TrafficFlowBulkEditView.as_view(), name='trafficflow_bulk_edit'),
    path('flows/bulk/delete/', TrafficFlowBulkDeleteView.as_view(), name='trafficflow_bulk_delete'),    path('flows/<int:pk>/', TrafficFlowEditView.as_view(), name='trafficflow'),
    path('flows/<int:pk>/changelog/', TrafficFlowEditView.as_view(), name='trafficflow_changelog'),]