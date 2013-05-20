import itertools

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from django.db import transaction
from django.template import RequestContext
from django.core import serializers
from django import forms as django_forms
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models as django_models
from django.conf import settings

from basicauth import models as basicauth_models
from basicauth import forms as basicauth_forms
from basicauth.decorators import login_required, admin_access

@require_GET
@admin_access
@login_required
def user_new(request):
    d = {}

    user_form = basicauth_forms.UserModelForm()

    d['user_form'] = user_form

    return render(request, 'basicauth/admin/user/form.html', d)

@transaction.commit_on_success
@require_POST
@admin_access
@login_required
def user_create(request):

    user_form = basicauth_forms.UserModelForm(request.POST)

    if user_form.is_valid():
        instance = user_form.save(commit=False)
        instance.set_password(user_form.cleaned_data['password'])
        instance.save()
        messages.info(request, 'Successfully added user')
        return redirect('user_list')
    else:
        d = {}
        d['user_form'] = user_form

        messages.error(request, 'Error adding user')

        return render(request, 'basicauth/admin/user/form.html', d)

@require_GET
@admin_access
@login_required
def user_edit(request, user_id):
    d = {}

    user = get_object_or_404(basicauth_models.User, pk=user_id)
    user_form = basicauth_forms.UserModelForm(instance=user)

    d['user'] = user
    d['user_form'] = user_form

    return render(request, 'basicauth/admin/user/form.html', d)

@transaction.commit_on_success
@require_POST
@admin_access
@login_required
def user_update(request, user_id):
    user = get_object_or_404(basicauth_models.User, pk=user_id)
    user_form = basicauth_forms.UserModelForm(request.POST, instance=user)
    user_password = user.password
    if request.POST['password'] == '' and \
       request.POST['password_confirm'] == '':
        # disable required field checks for password and
        # set old password when password, password_confirm
        # fields are blank
        user_form.fields['password'].required = False
        user_form.fields['password_confirm'].required = False

    if user_form.is_valid():
        # after this call, the model has password field set
        # to blank hence why we save user_password above
        m = user_form.save(commit=False)
        if user_form.fields['password'].required:
            m.set_password(user_form.cleaned_data['password'])
        else:
            # re-save old password
            m.password = user_password
        m.save()
        messages.info(request, 'Successfully updated user')
        return redirect('user_detail', user.id)
    else:
        d = {}
        d['user'] = user
        d['user_form'] = user_form
        messages.error(request, 'Error updating user')
        return render(
            request,
            'basicauth/admin/user/form.html',
            d)

@transaction.commit_on_success
@require_GET
@admin_access
@login_required
def user_delete(request, user_id):
    user = get_object_or_404(basicauth_models.User, pk=user_id)
    user_id = user.id
    user.delete()
    messages.info(request, 'Successfully deleted user')
    return redirect('user_list')

@require_GET
@admin_access
@login_required
def user_list(request):
    ordering_fields = [
        'id',
        'username',
        'email',
        'last_name',
        'first_name',
    ]
    ordering_form = common.OrderFieldForm(
        request.GET or {}, ordering_fields=ordering_fields)
    ordering_form.is_valid()

    search_term = request.GET.get('search_term', '')

    # Search user fields
    users = basicauth_models.User.objects.filter(
            django_models.Q(username__icontains=search_term)|
            django_models.Q(email__icontains=search_term)|
            django_models.Q(last_name__icontains=search_term)|
            django_models.Q(first_name__icontains=search_term)
        ).order_by(ordering_form.queryset_value()).all()

    # Search usergroup fields
    usergroups = basicauth_models.UserGroup.objects.filter(
        group__name__icontains=search_term).all()

    users = basicauth_models.User.objects.filter(
        id__in=list(
            itertools.chain(
                [ug.user.id for ug in usergroups],
                [u.id for u in users])))

    d = {}

    paginator, users_page, paginator_page_range = \
        common._get_paginator_data(request, users)

    d['users'] = users
    d['ordering_form'] = ordering_form
    d['paginator'] = paginator
    d['users_page'] = users_page
    d['paginator_page_range'] = paginator_page_range

    return render(
        request,
        'basicauth/admin/user/list.html',
        d)

@require_GET
@admin_access
@login_required
def user_detail(request, user_id):
    d = {}

    user = get_object_or_404(basicauth_models.User, pk=user_id)

    d['user'] = user

    return render(
        request,
        'basicauth/admin/user/detail.html',
        d)

@require_GET
@admin_access
@login_required
def ajax_usergroup_new(request, user_id):
    if request.is_ajax():
        user = get_object_or_404(basicauth_models.User, pk=user_id)
        usergroup_form = basicauth_forms.UserGroupModelForm(
            initial={ 'user': user })

        d = {}
        d['user'] = user
        d['usergroup_form'] = usergroup_form

        render_location = 'basicauth/admin/usergroup/form.html'

        html = common.HtmlTemplate(
            request=request,
            template_dictionary=d,
            template_location=render_location).get_string()
        response = common.JsonResponse(status="success", html=html)
        return response.send()
    else:
        raise Http404

@transaction.commit_on_success
@admin_access
@login_required
def ajax_usergroup_create(request):
    if request.is_ajax():
        usergroup_form = basicauth_forms.UserGroupModelForm(request.POST)
        if usergroup_form.is_valid():
            usergroup_form.save()
            messages.info(request,
                'Successfully added group for user')

            d = {}
            d['user'] = usergroup_form.instance.user

            render_location = \
                'basicauth/admin/usergroup/list.html'
            html = common.HtmlTemplate(
                request=request,
                template_dictionary=d,
                template_location=render_location).get_string()
            messages_html = common.HtmlTemplate(
                request=request,
                template_dictionary={},
                template_location='_messages.html').get_string()
            response = common.JsonResponse(
                status="success", html=html, messages=messages_html)
            return response.send()
        else:
            messages.error(request,
                'Error adding group for user')

            d = {}
            d['usergroup_form'] = usergroup_form
            d['user'] = usergroup_form.instance.user

            render_location = \
                'basicauth/admin/usergroup/form.html'

            html = common.HtmlTemplate(
                request=request,
                template_dictionary=d,
                template_location=render_location).get_string()
            messages_html = common.HtmlTemplate(
                request=request,
                template_dictionary={},
                template_location='_messages.html').get_string()
            response = common.JsonResponse(
                status="error", html=html, messages=messages_html)
            return response.send()
    else:
        raise Http404

@transaction.commit_on_success
@require_GET
@admin_access
@login_required
def usergroup_delete(request, usergroup_id):
    usergroup = get_object_or_404(basicauth_models.UserGroup, pk=usergroup_id)
    user = usergroup.user
    user_group_name = usergroup.group.name
    usergroup.delete()
    messages.info(request, 'Successfully removed group for user')
    if request.is_ajax():
        d = {}
        d['user'] = user
        render_location = 'basicauth/admin/usergroup/list.html'
        html = common.HtmlTemplate(
            request=request,
            template_dictionary=d,
            template_location=render_location).get_string()
        messages_html = common.HtmlTemplate(
            request=request,
            template_dictionary={},
            template_location='_messages.html').get_string()
        response = common.JsonResponse(
            status="success", html=html, messages=messages_html)
        return response.send()
    else:
        return redirect('user_detail', user.id)
