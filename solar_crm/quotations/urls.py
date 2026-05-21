from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.quotations_list_view,   name='quotations_list_view'),
    path('add/',                          views.quotations_add_view,    name='quotations_add_view'),
    path('<int:quotation_id>/',           views.quotations_detail_view, name='quotations_detail_view'),
    path('edit/<int:quotation_id>/',      views.quotations_edit_view,   name='quotations_edit_view'),
    path('delete/<int:quotation_id>/',    views.quotations_delete_view, name='quotations_delete_view'),
]