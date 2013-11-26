django_basicauth
================

sometimes I don't feel like using anything from django.contrib.user. this is really minimum viable.  use at your own risk.

Add as git submodule
--------------------

git submodule add ssh://rpq@winscores.com/home/rpq/.local/var/git/django_basicauth basicauth

2. Add imports and urls to your urls.py
--------------------

2 from django.views.generic.base import RedirectView
4 from django.conf import settings

url(r'^success$',
    RedirectView.as_view(url=settings.LOGIN_SUCCESS_DEFAULT_URL),
    name='root'),
url(r'^admin/login-redirect$',
    'basicauth.authentication.views.login_redirect',
    name='login_redirect'),
url(r'^admin/login$',
    'basicauth.authentication.views.login',
    name='login'),
url(r'^logout$',
    'basicauth.authentication.views.logout',
    name='logout'),

Configure LOGIN_SUCCESS_DEFAULT_URL
--------------------

Add basicauth to installed_apps setting and syncdb
--------------------

Copy /templates/basicauth/authentication/login.release.html 
to /templates/basicauth/authentication/login.custom.html
--------------------

Make symlink from login.custom.html (from previous step) to 
point from login.html (ie, ln -s login.custom.html login.html)
--------------------

Create directory for static files and template files and add to
STATICFILES_DIRS and TEMPLATE_DIRS respectively
--------------------

There is a generic layout.html in basicauth/templates/login.release.html.
Configure file for your usage (note you may need to add partials called
from this file.
--------------------
