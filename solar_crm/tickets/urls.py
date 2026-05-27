from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.tickets_list_view,        name='tickets_list_view'),
    path('add/',                    views.tickets_add_view,         name='tickets_add_view'),
    path('<int:ticket_id>/',        views.tickets_detail_view,      name='tickets_detail_view'),
    path('edit/<int:ticket_id>/',   views.tickets_edit_view,        name='tickets_edit_view'),
    path('delete/<int:ticket_id>/', views.tickets_delete_view,      name='tickets_delete_view'),
    path('export-leads/',           views.export_leads_excel,       name='export_leads_excel'),
    path('import-leads/',           views.import_leads_view,        name='import_leads_view'),
    path('download-template/',      views.download_import_template, name='download_import_template'),
    path('public/submit/',          views.public_ticket_submit,     name='public_ticket_submit'),
]