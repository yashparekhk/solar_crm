from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.payments_list_view,   name='payments_list_view'),
    path('add/',                     views.payments_add_view,    name='payments_add_view'),
    path('<int:payment_id>/',        views.payments_detail_view, name='payments_detail_view'),
    path('edit/<int:payment_id>/',   views.payments_edit_view,   name='payments_edit_view'),
    path('delete/<int:payment_id>/', views.payments_delete_view, name='payments_delete_view'),
]