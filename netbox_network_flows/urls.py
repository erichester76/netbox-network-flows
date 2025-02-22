from django.urls import path, include
from .views import TrafficFlowListView, TrafficFlowEditView, TrafficFlowImportView

urlpatterns = [
    path('flows/', TrafficFlowListView.as_view(), name='flow_list'),
    path('flows/add/', TrafficFlowEditView.as_view(), name='flow_add'),
    path('flows/<int:pk>/edit/', TrafficFlowEditView.as_view(), name='flow_edit'),
    path('flows/import/', TrafficFlowImportView.as_view(), name='flow_import'),
]