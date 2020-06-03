from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .views import custom_login, custom_dashboard, change_password, profile_about
# from .registration_views import ActivationView, \
#     RegistrationView, \
#     PasswordRecoveryView

urlpatterns = [

    url(r'^captcha/', include('captcha.urls')),

    url(r'^$', custom_dashboard, name='custom_dashboard'),
    url(r'^home/$', custom_dashboard, name='custom_dashboard'),
    url(r'^accounts/$', custom_login, name='custom_login'),
    url(r'^accounts/login/$', custom_login, name='custom_login'),
    url(r'^accounts/profile_about/$', profile_about, name='profile_about'),

    url(r'^accounts/logout/$',
        auth_views.logout,
        {'template_name': 'accounts/logout.html', 'next_page': '/accounts/login/'},
        name='auth_logout'),

    # url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    # url(r'^accounts/activate/(?P<activation_key>[-:\w]+)/$', ActivationView.as_view(), name='registration_activate'),


    # url(r'^accounts/password_recovery/$', PasswordRecoveryView.as_view(), name='password_recovery'),
    url(r'^accounts/change_password/(?P<secret_key>[-:\w]+)/$', change_password, name='change_password'),

]

