from django.urls import path
from . import views
from .models import TrafficFlow, ServiceEndpoint

app_name = 'netbox_network_flows'

urlpatterns = [
    
    path('flows/', views.TrafficFlowListView.as_view(), name='trafficflow_list'),
    path('flows/add/', views.TrafficFlowEditView.as_view(), name='trafficflow_add'),
    path('flows/<int:pk>/edit/', views.TrafficFlowEditView.as_view(), name='trafficflow_edit'),
    path('flows/<int:pk>/delete/', views.TrafficFlowEditView.as_view(), name='trafficflow_delete'),
    path('flows/bulk/import/', views.TrafficFlowImportView.as_view(), name='trafficflow_import'),
    path('flows/bulk/edit/', views.TrafficFlowBulkEditView.as_view(), name='trafficflow_bulk_edit'),
    path('flows/bulk/delete/', views.TrafficFlowBulkDeleteView.as_view(), name='trafficflow_bulk_delete'),    
    path('flows/<int:pk>/changelog/', views.TrafficFlowChangelogView.as_view(), name='trafficflow_changelog', kwargs={'model': TrafficFlow}),
    
    # ServiceEndpoints URLs
    path('service-endpoints/', views.ServiceEndpointListView.as_view(), name='serviceendpoint_list'),
    path('service-endpoints/add/', views.ServiceEndpointEditView.as_view(), name='serviceendpoint_add'),
    path('service-endpoints/<int:pk>/edit/', views.ServiceEndpointEditView.as_view(), name='serviceendpoint_edit'),
    path('service-endpoints/<int:pk>/delete/', views.ServiceEndpointDeleteView.as_view(), name='serviceendpoint_delete'),
    path('service-endpoints/edit/', views.ServiceEndpointBulkEditView.as_view(), name='serviceendpoint_bulk_edit'),
    path('service-endpoints/import/', views.ServiceEndpointImportView.as_view(), name='serviceendpoint_import'),
    path('service-endpoints/edit/', views.ServiceEndpointBulkEditView.as_view(), name='serviceendpoint_bulk_edit'),
    path('service-endpoints/delete/', views.ServiceEndpointBulkDeleteView.as_view(), name='serviceendpoint_bulk_delete'),
    path('service-endpoints/<int:pk>/changelog/', views.ServiceEndpointChangelogView.as_view(), name='serviceendpoint_changelog', kwargs={'model': ServiceEndpoint}),
      
]