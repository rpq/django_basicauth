from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    'basicauth.views_admin',

'''
These should go into the your project's urls.py:

   url(r'^/?$',
        RedirectView.as_view(url=settings.LOGIN_SUCCESS_DEFAULT_URL),
        name='access_root'),
   url(r'^success$',
        RedirectView.as_view(url=settings.LOGIN_SUCCESS_DEFAULT_URL),
        name='root'),
   url(r'^login-redirect$',
        'basicauth.authentication.views.login_redirect',
        name='login_redirect'),
   url(r'^login$',
        'basicauth.authentication.views.login',
        name='login'),
   url(r'^logout$',
        'basicauth.authentication.views.logout',
        name='logout'),
'''

'''
    url(r'^register$', 'basicauth.authentication.views.register',
        name='register'),
    url(r'^register$', 'basicauth.authentication.views.register',
        name='register'),
    url(r'^verify-email/(?P<verify_id>[a-zA-Z-]+)$',
        'basicauth.authentication.views.register_email_verify',
        name='register_email_verify'),
'''
)
