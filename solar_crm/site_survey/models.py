from django.db import models
from django.conf import settings
from leads.models import Lead
from customers.models import Customer

ROOF_TYPE_CHOICES = [
    ('rcc',         'RCC / Concrete'),
    ('tiles',       'Clay Tiles'),
    ('metal_sheet', 'Metal Sheet'),
    ('asbestos',    'Asbestos'),
    ('other',       'Other'),
]

SHADOW_ANALYSIS_CHOICES = [
    ('none',    'No Shadow'),
    ('partial', 'Partial Shadow'),
    ('heavy',   'Heavy Shadow'),
]

SURVEY_STATUS_CHOICES = [
    ('scheduled',  'Scheduled'),
    ('completed',  'Completed'),
    ('cancelled',  'Cancelled'),
    ('revisit',    'Revisit Required'),
]

FEASIBILITY_CHOICES = [
    ('feasible',     'Feasible'),
    ('not_feasible', 'Not Feasible'),
    ('partially',    'Partially Feasible'),
    ('under_review', 'Under Review'),
]

PHASE_CHOICES = [
    ('single', 'Single Phase'),
    ('three',  'Three Phase'),
]

DISCOM_CHOICES = [
    ('dgvcl', 'DGVCL'),
    ('mgvcl', 'MGVCL'),
    ('pgvcl', 'PGVCL'),
    ('ugvcl', 'UGVCL'),
    ('other', 'Other'),
]


class SiteSurvey(models.Model):

    # ── Relationships ──
    lead     = models.ForeignKey(
        Lead, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='site_surveys', verbose_name='Related Lead',
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='site_surveys', verbose_name='Related Customer',
    )
    surveyor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='surveys_conducted', verbose_name='Surveyor',
    )

    # ── Basic Info ──
    survey_date    = models.DateField(verbose_name='Survey Date')
    survey_address = models.TextField(verbose_name='Site Address')
    status         = models.CharField(max_length=20, choices=SURVEY_STATUS_CHOICES, default='scheduled')
    feasibility    = models.CharField(max_length=20, choices=FEASIBILITY_CHOICES, default='under_review')

    # ── Roof Details ──
    roof_type      = models.CharField(max_length=20, choices=ROOF_TYPE_CHOICES, blank=True)
    roof_area_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Available Roof Area (sq ft)')
    shadow_analysis = models.CharField(max_length=20, choices=SHADOW_ANALYSIS_CHOICES, blank=True)
    roof_age_years = models.PositiveIntegerField(null=True, blank=True, verbose_name='Roof Age (years)')
    roof_condition = models.CharField(max_length=100, blank=True, verbose_name='Roof Condition')

    # ── Electrical Details ──
    monthly_bill       = models.DecimalField(        # ← NEW FIELD
        max_digits=8, decimal_places=2,
        null=True, blank=True,
        verbose_name='Monthly Electricity Bill (₹)',
    )
    existing_load_kw   = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Existing Load (kW)')
    sanctioned_load_kw = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Sanctioned Load (kW)')
    monthly_units      = models.PositiveIntegerField(null=True, blank=True, verbose_name='Monthly Consumption (Units)')
    phase              = models.CharField(max_length=10, choices=PHASE_CHOICES, blank=True)
    discom             = models.CharField(max_length=20, choices=DISCOM_CHOICES, blank=True, verbose_name='DISCOM / Electricity Board')
    meter_number       = models.CharField(max_length=50, blank=True, verbose_name='Electricity Meter Number')
    consumer_number    = models.CharField(max_length=50, blank=True, verbose_name='Consumer Number')

    # ── Solar Recommendation ──
    recommended_system_kw      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Recommended System Size (kW)')
    recommended_panels         = models.PositiveIntegerField(null=True, blank=True, verbose_name='No. of Panels Recommended')
    estimated_generation_units = models.PositiveIntegerField(null=True, blank=True, verbose_name='Estimated Monthly Generation (Units)')
    subsidy_eligible           = models.BooleanField(default=False, verbose_name='Eligible for PM Surya Ghar Subsidy')
    estimated_subsidy          = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Estimated Subsidy Amount (₹)')

    # ── Notes ──
    observations   = models.TextField(blank=True, verbose_name='Site Observations')
    recommendations = models.TextField(blank=True, verbose_name='Surveyor Recommendations')
    internal_notes = models.TextField(blank=True, verbose_name='Internal Notes')

    # ── Timestamps ──
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_client_name(self):
        if self.lead:
            return self.lead.name
        if self.customer:
            return self.customer.name
        return 'Unknown'

    def __str__(self):
        return f"Survey — {self.get_client_name()} ({self.survey_date})"

    class Meta:
        verbose_name        = 'Site Survey'
        verbose_name_plural = 'Site Surveys'
        ordering            = ['-survey_date', '-created_at']