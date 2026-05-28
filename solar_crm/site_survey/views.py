from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    SiteSurvey,
    SURVEY_STATUS_CHOICES,
    FEASIBILITY_CHOICES,
    ROOF_TYPE_CHOICES,
    SHADOW_ANALYSIS_CHOICES,
    PHASE_CHOICES,
    DISCOM_CHOICES,
)
from leads.models import Lead
from customers.models import Customer
from accounts.models import CustomUser
from accounts.permissions import employee_or_admin_required

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def survey_list_view(request):
    search_query  = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    surveys = SiteSurvey.objects.all().order_by('-survey_date')

    if search_query:
        surveys = surveys.filter(
            lead__name__icontains=search_query
        ) | SiteSurvey.objects.filter(
            customer__name__icontains=search_query
        ) | SiteSurvey.objects.filter(
            survey_address__icontains=search_query
        )

    if status_filter:
        surveys = surveys.filter(status=status_filter)

    context = {
        'surveys_list':   surveys,
        'total_count':    surveys.count(),
        'status_filter':  status_filter,
        'search_query':   search_query,
        'status_choices': SURVEY_STATUS_CHOICES,
        'page_title':     'Site Surveys',
    }
    return render(request, 'site_survey/survey_list.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def survey_detail_view(request, survey_id):
    survey_instance = get_object_or_404(SiteSurvey, pk=survey_id)
    context = {
        'survey_instance': survey_instance,
        'page_title':      f'Survey — {survey_instance.get_client_name()}',
    }
    return render(request, 'site_survey/survey_detail.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def survey_add_view(request):
    leads_list     = Lead.objects.all().order_by('name')
    customers_list = Customer.objects.all().order_by('name')
    surveyors_list = CustomUser.objects.filter(role__in=['admin', 'employee'])

    if request.method == 'POST':
        new_survey = SiteSurvey.objects.create(
            lead_id            = request.POST.get('lead') or None,
            customer_id        = request.POST.get('customer') or None,
            surveyor_id        = request.POST.get('surveyor') or None,
            survey_date        = request.POST.get('survey_date'),
            survey_address     = request.POST.get('survey_address', '').strip(),
            status             = request.POST.get('status', 'scheduled'),
            feasibility        = request.POST.get('feasibility', 'under_review'),
            roof_type          = request.POST.get('roof_type', ''),
            roof_area_sqft     = request.POST.get('roof_area_sqft') or None,
            shadow_analysis    = request.POST.get('shadow_analysis', ''),
            roof_age_years     = request.POST.get('roof_age_years') or None,
            roof_condition     = request.POST.get('roof_condition', '').strip(),
            monthly_bill       = request.POST.get('monthly_bill') or None,   # ← NEW
            existing_load_kw   = request.POST.get('existing_load_kw') or None,
            sanctioned_load_kw = request.POST.get('sanctioned_load_kw') or None,
            monthly_units      = request.POST.get('monthly_units') or None,
            phase              = request.POST.get('phase', ''),
            discom             = request.POST.get('discom', ''),
            meter_number       = request.POST.get('meter_number', '').strip(),
            consumer_number    = request.POST.get('consumer_number', '').strip(),
            recommended_system_kw      = request.POST.get('recommended_system_kw') or None,
            recommended_panels         = request.POST.get('recommended_panels') or None,
            estimated_generation_units = request.POST.get('estimated_generation_units') or None,
            subsidy_eligible           = bool(request.POST.get('subsidy_eligible')),
            estimated_subsidy          = request.POST.get('estimated_subsidy') or None,
            observations       = request.POST.get('observations', '').strip(),
            recommendations    = request.POST.get('recommendations', '').strip(),
            internal_notes     = request.POST.get('internal_notes', '').strip(),
        )
        messages.success(request, f'Site survey for "{new_survey.get_client_name()}" created successfully!')
        return redirect('survey_detail_view', survey_id=new_survey.pk)

    context = {
        'leads_list':          leads_list,
        'customers_list':      customers_list,
        'surveyors_list':      surveyors_list,
        'status_choices':      SURVEY_STATUS_CHOICES,
        'feasibility_choices': FEASIBILITY_CHOICES,
        'roof_type_choices':   ROOF_TYPE_CHOICES,
        'shadow_choices':      SHADOW_ANALYSIS_CHOICES,
        'phase_choices':       PHASE_CHOICES,
        'discom_choices':      DISCOM_CHOICES,
        'page_title':          'New Site Survey',
    }
    return render(request, 'site_survey/survey_add.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def survey_edit_view(request, survey_id):
    survey_instance = get_object_or_404(SiteSurvey, pk=survey_id)
    leads_list      = Lead.objects.all().order_by('name')
    customers_list  = Customer.objects.all().order_by('name')
    surveyors_list  = CustomUser.objects.filter(role__in=['admin', 'employee'])

    if request.method == 'POST':
        survey_instance.lead_id            = request.POST.get('lead') or None
        survey_instance.customer_id        = request.POST.get('customer') or None
        survey_instance.surveyor_id        = request.POST.get('surveyor') or None
        survey_instance.survey_date        = request.POST.get('survey_date')
        survey_instance.survey_address     = request.POST.get('survey_address', '').strip()
        survey_instance.status             = request.POST.get('status', 'scheduled')
        survey_instance.feasibility        = request.POST.get('feasibility', 'under_review')
        survey_instance.roof_type          = request.POST.get('roof_type', '')
        survey_instance.roof_area_sqft     = request.POST.get('roof_area_sqft') or None
        survey_instance.shadow_analysis    = request.POST.get('shadow_analysis', '')
        survey_instance.roof_age_years     = request.POST.get('roof_age_years') or None
        survey_instance.roof_condition     = request.POST.get('roof_condition', '').strip()
        survey_instance.monthly_bill       = request.POST.get('monthly_bill') or None   # ← NEW
        survey_instance.existing_load_kw   = request.POST.get('existing_load_kw') or None
        survey_instance.sanctioned_load_kw = request.POST.get('sanctioned_load_kw') or None
        survey_instance.monthly_units      = request.POST.get('monthly_units') or None
        survey_instance.phase              = request.POST.get('phase', '')
        survey_instance.discom             = request.POST.get('discom', '')
        survey_instance.meter_number       = request.POST.get('meter_number', '').strip()
        survey_instance.consumer_number    = request.POST.get('consumer_number', '').strip()
        survey_instance.recommended_system_kw      = request.POST.get('recommended_system_kw') or None
        survey_instance.recommended_panels         = request.POST.get('recommended_panels') or None
        survey_instance.estimated_generation_units = request.POST.get('estimated_generation_units') or None
        survey_instance.subsidy_eligible           = bool(request.POST.get('subsidy_eligible'))
        survey_instance.estimated_subsidy          = request.POST.get('estimated_subsidy') or None
        survey_instance.observations    = request.POST.get('observations', '').strip()
        survey_instance.recommendations = request.POST.get('recommendations', '').strip()
        survey_instance.internal_notes  = request.POST.get('internal_notes', '').strip()
        survey_instance.save()

        messages.success(request, 'Site survey updated successfully!')
        return redirect('survey_detail_view', survey_id=survey_instance.pk)

    context = {
        'survey_instance':     survey_instance,
        'leads_list':          leads_list,
        'customers_list':      customers_list,
        'surveyors_list':      surveyors_list,
        'status_choices':      SURVEY_STATUS_CHOICES,
        'feasibility_choices': FEASIBILITY_CHOICES,
        'roof_type_choices':   ROOF_TYPE_CHOICES,
        'shadow_choices':      SHADOW_ANALYSIS_CHOICES,
        'phase_choices':       PHASE_CHOICES,
        'discom_choices':      DISCOM_CHOICES,
        'page_title':          f'Edit Survey — {survey_instance.get_client_name()}',
    }
    return render(request, 'site_survey/survey_edit.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def survey_delete_view(request, survey_id):
    survey_instance = get_object_or_404(SiteSurvey, pk=survey_id)
    if request.method == 'POST':
        survey_instance.delete()
        messages.success(request, 'Site survey deleted successfully!')
        return redirect('survey_list_view')
    context = {
        'survey_instance': survey_instance,
        'page_title':      'Delete Survey',
    }
    return render(request, 'site_survey/survey_delete.html', context)