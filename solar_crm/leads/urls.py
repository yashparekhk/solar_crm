from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.leads_list_view,    name='leads_list_view'),
    path('add/',                      views.leads_add_view,     name='leads_add_view'),
    path('<int:lead_id>/',            views.leads_detail_view,  name='leads_detail_view'),
    path('edit/<int:lead_id>/',       views.leads_edit_view,    name='leads_edit_view'),
    path('delete/<int:lead_id>/',     views.leads_delete_view,  name='leads_delete_view'),
    path('convert/<int:lead_id>/',    views.leads_convert_view, name='leads_convert_view'),
]