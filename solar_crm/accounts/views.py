from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser


def register_view(request):
    user_exists = CustomUser.objects.exists()
    if user_exists and not (
        request.user.is_authenticated and request.user.role == 'admin'
    ):
        messages.info(request, 'Registration is closed. Please contact your administrator.')
        return redirect('login_view')

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save()
            messages.success(request, f'Account created for {new_user.get_full_name()}! Please login.')
            return redirect('login_view')
    else:
        registration_form = UserRegistrationForm()

    context = {
        'registration_form': registration_form,
        'page_title':        'Register',
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_view')

    if request.method == 'POST':
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            authenticated_user = login_form.get_user()
            login(request, authenticated_user)
            messages.success(
                request,
                f'Welcome back, {authenticated_user.first_name or authenticated_user.username}!'
            )
            return redirect('dashboard_view')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        login_form = UserLoginForm()

    user_exists = CustomUser.objects.exists()
    context = {
        'login_form':  login_form,
        'user_exists': user_exists,
        'page_title':  'Login',
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login_view')


@login_required(login_url='/accounts/login/')
def profile_view(request):
    """Display and edit user profile."""
    current_user = request.user

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip().capitalize()
        last_name  = request.POST.get('last_name', '').strip().capitalize()
        email      = request.POST.get('email', '').strip()
        phone      = request.POST.get('phone', '').strip()
        address    = request.POST.get('address', '').strip()

        # Update user fields
        current_user.first_name = first_name
        current_user.last_name  = last_name
        current_user.email      = email
        current_user.phone      = phone
        current_user.address    = address
        current_user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')

    context = {
        'page_title':   'My Profile',
        'current_user': current_user,
    }
    return render(request, 'accounts/profile.html', context)


def forgot_password_view(request):
    """Step 1 — Enter email to receive OTP."""
    if request.method == 'POST':
        email_input = request.POST.get('email', '').strip()

        # Find user by email safely
        user_found = CustomUser.objects.filter(email=email_input).first()

        if not user_found:
            messages.error(request, 'No account found with this email address.')
            return render(request, 'accounts/forgot_password.html', {
                'page_title': 'Forgot Password'
            })

        # Generate 6 digit OTP
        import random
        otp_code = str(random.randint(100000, 999999))

        # Store OTP and email in session
        request.session['reset_otp']   = otp_code
        request.session['reset_email'] = email_input

        # Professional email content
        email_subject = 'Solar CRM — Password Reset OTP'
        email_message = f"""
Dear {user_found.first_name or user_found.username},

We received a request to reset your Solar CRM account password.

Your One-Time Password (OTP) is:

    {otp_code}

This OTP is valid for 10 minutes only.

If you did not request a password reset, please ignore this email.
Your account remains secure.

Regards,
Solar CRM Team
        """.strip()

        # Send real email
        from django.core.mail import send_mail
        from django.conf import settings

        try:
            send_mail(
                subject        = email_subject,
                message        = email_message,
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [email_input],
                fail_silently  = False,
            )
            messages.success(
                request,
                f'OTP sent successfully to {email_input}. Please check your inbox.'
            )
            return redirect('verify_otp_view')

        except Exception as email_error:
            print(f"Email error: {email_error}")
            messages.error(
                request,
                'Failed to send OTP. Please check your email configuration.'
            )
            return render(request, 'accounts/forgot_password.html', {
                'page_title': 'Forgot Password'
            })

    return render(request, 'accounts/forgot_password.html', {
        'page_title': 'Forgot Password'
    })
    
def verify_otp_view(request):
    """Step 2 — Verify OTP."""
    if 'reset_email' not in request.session:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('forgot_password_view')

    if request.method == 'POST':
        entered_otp  = request.POST.get('otp', '').strip()
        session_otp  = request.session.get('reset_otp', '')

        if entered_otp == session_otp:
            request.session['otp_verified'] = True
            messages.success(request, 'OTP verified! Now set your new password.')
            return redirect('reset_password_view')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'accounts/verify_otp.html', {'page_title': 'Verify OTP'})


def reset_password_view(request):
    """Step 3 — Set new password."""
    if not request.session.get('otp_verified'):
        messages.error(request, 'Please verify OTP first.')
        return redirect('forgot_password_view')

    if request.method == 'POST':
        import re
        new_password     = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if len(new_password) > 15:
            messages.error(request, 'Password must be maximum 15 characters.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        if not re.search(r'[A-Z]', new_password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        if not re.search(r'[a-z]', new_password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        if not re.search(r'[0-9]', new_password):
            messages.error(request, 'Password must contain at least one number.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})

        # Use filter().first() to avoid MultipleObjectsReturned
        reset_email   = request.session.get('reset_email')
        user_to_reset = CustomUser.objects.filter(email=reset_email).first()

        if user_to_reset:
            user_to_reset.set_password(new_password)
            user_to_reset.save()

            # Clear session
            request.session.pop('reset_otp',      None)
            request.session.pop('reset_email',     None)
            request.session.pop('otp_verified',    None)

            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login_view')
        else:
            messages.error(request, 'User not found. Please try again.')
            return redirect('forgot_password_view')

    return render(request, 'accounts/reset_password.html', {'page_title': 'Reset Password'})