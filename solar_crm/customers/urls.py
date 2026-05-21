from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.customers_list_view,   name='customers_list_view'),
    path('add/',                        views.customers_add_view,    name='customers_add_view'),
    path('<int:customer_id>/',          views.customers_detail_view, name='customers_detail_view'),
    path('edit/<int:customer_id>/',     views.customers_edit_view,   name='customers_edit_view'),
    path('delete/<int:customer_id>/',   views.customers_delete_view, name='customers_delete_view'),
]