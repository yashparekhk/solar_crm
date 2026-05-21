from django.urls import path
from . import views

urlpatterns = [
    path('register/',        views.register_view,        name='register_view'),
    path('login/',           views.login_view,            name='login_view'),
    path('logout/',          views.logout_view,           name='logout_view'),
    path('profile/',         views.profile_view,          name='profile_view'),
    path('forgot-password/', views.forgot_password_view,  name='forgot_password_view'),
    path('verify-otp/',      views.verify_otp_view,       name='verify_otp_view'),
    path('reset-password/',  views.reset_password_view,   name='reset_password_view'),
]