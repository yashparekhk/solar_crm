from .permissions import get_user_permissions


def user_permissions(request):
    """
    Injects user permissions into every template context.
    Access in templates as: {{ perms_map.can_delete_lead }}
    """
    if request.user.is_authenticated:
        return {
            'perms_map': get_user_permissions(request.user)
        }
    return {'perms_map': {}}