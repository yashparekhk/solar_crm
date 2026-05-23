def global_context(request):
    """Adds global variables available in every template including base.html"""
    total_leads = 0
    if request.user.is_authenticated:
        try:
            from leads.models import Lead
            total_leads = Lead.objects.count()
        except Exception:
            total_leads = 0
    return {
        'global_total_leads': total_leads,
    }