from django.contrib import admin
from .models import SiteSurvey


@admin.register(SiteSurvey)
class SiteSurveyAdmin(admin.ModelAdmin):
    list_display  = [
        'get_client_name', 'surveyor', 'survey_date',
        'status', 'feasibility', 'recommended_system_kw'
    ]
    list_filter   = ['status', 'feasibility', 'roof_type', 'discom']
    search_fields = ['lead__name', 'customer__name', 'survey_address']
    ordering      = ['-survey_date']
    list_per_page = 25