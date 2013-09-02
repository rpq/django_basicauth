from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse

from basicauth import models
from basicauth import helpers

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if _logged_in(request):
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return helpers.json_redirect(reverse('login'))
            else:
                messages.error(request,
                    'Please login to view this page.')
                return redirect('login')
    return wrapper

'''
# for group related stuff

def admin_access(func):
    def wrapper(request, *args, **kwargs):
        if _logged_in(request):
            logged_in_user_id = \
                request.session.get('logged_in_user_id', None)
            if logged_in_user_id is None:
                return _display_access_message_and_redirect(request)

            try:
                user = models.User.objects.get(pk=logged_in_user_id)
                if user.is_admin():
                    return func(request, *args, **kwargs)
                else:
                    return _display_access_message_and_redirect(
                        request)
            except models.User.DoesNotExist:
                return _display_access_message_and_redirect(request)
        else:
            if request.is_ajax():
                return helpers.json_redirect(reverse('login'))
            else:
                messages.error(request, 'Please login to view this page.')
                return redirect('login')
    return wrapper
'''

def _logged_in(request):
    if request.session.get('logged_in_user_id', None) is not None:
        return True
    else:
        return False

def _display_access_message_and_redirect(request, access='admin'):
    request.session['last_requested_page'] = request.path
    messages.error(request, 
        'Must have %s access to view this page. %s' % \
        (access, request.path,))
    return redirect('login')
