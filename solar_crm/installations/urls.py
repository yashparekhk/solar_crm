from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.installations_list_view,   name='installations_list_view'),
    path('add/',                           views.installations_add_view,    name='installations_add_view'),
    path('<int:installation_id>/',         views.installations_detail_view, name='installations_detail_view'),
    path('edit/<int:installation_id>/',    views.installations_edit_view,   name='installations_edit_view'),
    path('delete/<int:installation_id>/',  views.installations_delete_view, name='installations_delete_view'),
]