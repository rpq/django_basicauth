# django_basicauth

Sometimes I do not feel like using anything from django.contrib.user. This is really minimum viable alternative.  Use at your own risk.

### Add as git submodule

git submodule add ssh://rpq@winscores.com/home/rpq/.local/var/git/django_basicauth basicauth

### Add 'basicauth' to INSTALLED_APPS setting and syncdb

### Update urls.py

```
from django.views.generic.base import RedirectView
from django.conf import settings

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
```

### Update settings.py

 * Configure LOGIN_SUCCESS_DEFAULT_URL = '/' (or whatever you want the
   redirect to be)

 * Create directory for static files and template files and add to
STATICFILES_DIRS and TEMPLATE_DIRS respectively

### Update template files

 * There is a generic example login.html file in 
   basicauth/templates/login.release.html. Symlink it or copy it.
     * Copy /templates/basicauth/authentication/login.release.html 
       to /templates/basicauth/authentication/login.custom.html
     * Make symlink from login.custom.html (from previous step) to 
       point from login.html (ie, ln -s login.custom.html login.html)

### Other notes

 * Decorators (ie, login_required, etc) are in decorators.py.
