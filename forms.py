from django import forms
from django.http import QueryDict

from basicauth import models

class UserModelForm(forms.ModelForm):

    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = (
            'username', 'password', 'password_confirm', 'email',
            'first_name', 'last_name',)
        widgets = { 'password': forms.PasswordInput, }

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean(self):
        cleaned_data = super(UserModelForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            msg = "Password and Password Confirmation fields do not match"
            self._errors["password"] = self.error_class([msg])
            self._errors["password_confirm"] = self.error_class([msg])
            del self.cleaned_data['password']
            del self.cleaned_data['password_confirm']
        return cleaned_data

class UserGroupModelForm(forms.ModelForm):

    class Meta:
        model = models.UserGroup
        fields = ('user', 'group',)
        widgets = { 'user': forms.HiddenInput, }

    '''
    # limit one group per user
    def clean(self):
        cleaned_data = \
            super(UserGroupModelForm, self).clean()
        if cleaned_data['user'].has_a_group():
            msg = 'User is already in the {0} group'.format(
                cleaned_data['user'].get_group())
            self._errors['group'] = self.error_class([msg])
        return cleaned_data
    '''
