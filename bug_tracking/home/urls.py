from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "home"
urlpatterns = [
    path('', views.home, name='principal'),
    path('login', views.login, name='login'),
    
    path('exit', views.exit, name='exit'),
    path('signup', views.signup, name='signup'),

    path('password_reset', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('check-username-availability/', views.check_username_availability, name='check_username_availability'),
    path('check-email-availability/', views.check_email_availability, name='check_email_availability'),


]
