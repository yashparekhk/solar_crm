from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.tasks_list_view,   name='tasks_list_view'),
    path('add/',                views.tasks_add_view,    name='tasks_add_view'),
    path('<int:pk>/edit/',      views.tasks_edit_view,   name='tasks_edit_view'),
    path('<int:pk>/delete/',    views.tasks_delete_view, name='tasks_delete_view'),

    # AJAX
    path('<int:pk>/complete/',  views.tasks_complete_api, name='tasks_complete_api'),
    path('<int:pk>/status/',    views.tasks_status_api,   name='tasks_status_api'),
    path('api/widget/',         views.tasks_widget_api,   name='tasks_widget_api'),
]