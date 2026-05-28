from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.survey_list_view,   name='survey_list_view'),
    path('add/',                    views.survey_add_view,    name='survey_add_view'),
    path('<int:survey_id>/',        views.survey_detail_view, name='survey_detail_view'),
    path('edit/<int:survey_id>/',   views.survey_edit_view,   name='survey_edit_view'),
    path('delete/<int:survey_id>/', views.survey_delete_view, name='survey_delete_view'),
]