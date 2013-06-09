from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction

from basicauth.decorators import login_required, admin_access, _logged_in
from basicauth import models as basicauth_models
from basicauth.authentication import forms
from basicauth.forms import UserModelForm

def login(request):
    if request.POST:
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            authenticated = basicauth_models.User.authenticate(
                username, password)
            if authenticated:
                user = \
                    basicauth_models.User.objects.get(
                        username=username)
                messages.info(request, 'Successfully logged in')
                request.session['logged_in_user_id'] = user.id
                return redirect('login_redirect')
        messages.error(request, 'Invalid username/password')
        return render(request, 'basicauth/authentication/login.html',
            { 'login_form': login_form })
    else:
        if _logged_in(request):
            user = get_object_or_404(
                basicauth_models.User,
                pk=request.session.get('logged_in_user_id'))
            messages.info(request,
                'You are already logged in as %s' % \
                user.username)
        login_form = forms.LoginForm()
        return render(request, 'basicauth/authentication/login.html',
            { 'login_form': login_form })

@transaction.commit_on_success
def logout(request):
    if request.session.pop('logged_in_user_id', None) is not None:
        messages.info(request, 'Successfully logged out')
    return redirect('login')

def login_redirect(request):
    if _logged_in(request):
        # if it's the case that the user existed once,
        # user logged in, and user was deleted while still
        # having an active session
        user = basicauth_models.User.objects.filter(
            pk=request.session.get('logged_in_user_id'))
        if user.exists():
            return redirect('userprofile_detail', user[0].username)
        else:
            request.session.pop('logged_in_user_id', None)
    return redirect('login')

@transaction.commit_on_success
def register(request):
    if request.POST:
        user_model_form = UserModelForm(request.POST)
        if user_model_form.is_valid():
            user = user_model_form.save(commit=False)
            user.set_password(
                user_model_form.cleaned_data['password'].encode(
                    'utf-8'))
            user.save()
            user.send_verify_email()
            messages.info(request, 'Successfully logged in')
            request.session['logged_in_user_id'] = user.id
            return redirect('login_redirect')
        else:
            d = dict(form=user_model_form)
            return render(request,
                'basicauth/authentication/register.html', d)
    else:
        d = {}
        d['form'] = UserModelForm()
        return render(request,
            'basicauth/authentication/register.html', d)

@transaction.commit_on_success
def register_email_verify(request, verify_id):
    u = get_object_or_404(basicauth_models.User,
        verify_id=verify_id)
    u.verify()
    u.save()
    messages.info(request,
        'We have successfully verified your email address.')
    return redirect('userprofile_detail', u.username)
