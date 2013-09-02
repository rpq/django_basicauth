django_basicauth
================

sometimes I don't feel like using anything from django.contrib.user. this is really minimum viable.  use at your own risk.

1. add git submodule as 'basicauth' app
1. setup ROOT_DEFAULT to point to url for successful login
1. copy and configure url dispatcher
    url(r'^admin$',
        RedirectView.as_view(url=settings.ROOT_DEFAULT),
        name='root'),
    url(r'^admin/login-redirect$',
        'basicauth.authentication.views.login_redirect',
        name='login_redirect'),
    url(r'^admin/login$',
        'basicauth.authentication.views.login',
        name='login'),
    url(r'^admin/logout$',
        'basicauth.authentication.views.logout',
        name='logout'),
