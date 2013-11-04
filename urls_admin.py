from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    'basicauth.views_admin',

    url(r'^$',
        RedirectView.as_view(url='/admin/basicauth/user/list'),
        name='basicauth_root'),
    url(r'/user/new$', 'user_new', name='user_new'),
    url(r'/user/create$', 'user_create', name='user_create'),
    url(r'/user/list$', 'user_list', name='user_list'),
    url(r'/user/(?P<user_id>\d+)/detail$',
        'user_detail', name='user_detail'),
    url(r'/user/(?P<user_id>\d+)/edit$',
        'user_edit', name='user_edit'),
    url(r'/user/(?P<user_id>\d+)/update$',
        'user_update', name='user_update'),
    url(r'/user/(?P<user_id>\d+)/delete$',
        'user_delete', name='user_delete'),

    url(r'/user/(?P<user_id>\d+)/usergroup/new$',
        'ajax_usergroup_new', name='ajax_usergroup_new'),
    url(r'/usergroup/create$',
        'ajax_usergroup_create', name='ajax_usergroup_create'),
    url(r'/usergroup/' \
        '(?P<usergroup_id>\d+)/delete$',
        'usergroup_delete', name='usergroup_delete'),

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
