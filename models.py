import bcrypt

from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators

from basicauth.helpers import CreatedUpdated

class User(CreatedUpdated):
    username = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        help_text='' \
            'Minimum of 3 characters, maximum of 20 characters, ' \
            'containing characters and numbers.',
        validators=[validators.MinLengthValidator(3)]
    )
    password = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(7),
            validators.RegexValidator(
                regex=r'[0-9]',
                message='Must have at least one number'),
            validators.RegexValidator(
                regex=r'[a-zA-Z]',
                message='Must have at least one character'),
        ]
    )
    email = models.EmailField(
        max_length=250, null=False, blank=False, unique=True)
    first_name = models.CharField(
        max_length=250, null=False, blank=False)
    last_name = models.CharField(
        max_length=250, null=False, blank=False)

    @classmethod
    def authenticate(cls, username, password_string):
        encoded_password_string = password_string.encode('utf-8')
        try:
            user = cls.objects.get(username=username)
            input_password = bcrypt.hashpw(
                encoded_password_string, user.password.encode('utf-8'))
            return user.password == input_password
        except cls.DoesNotExist:
            return None

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name,)

    def set_password(self, password_string):
        self.password = bcrypt.hashpw(
            password_string, bcrypt.gensalt())

    def has_a_group(self):
        return self.usergroup_set.all().count() > 0

    def has_child(self, child):
        return child in self.children.all()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode(self.full_name)

class Permission(CreatedUpdated):
    name = models.CharField(max_length=250, null=False, blank=False)
    display_name = models.CharField(max_length=250, null=False, blank=False)

    def __unicode__(self):
        return self.name

class Group(CreatedUpdated):
    name = models.CharField(max_length=250, null=False, blank=False)
    display_name = models.CharField(max_length=250, null=False, blank=False)

    def __unicode__(self):
        return self.name

class UserPermission(CreatedUpdated):
    user = models.ForeignKey(User)
    permission = models.ForeignKey(Permission)

    class Meta:
        unique_together = ('user', 'permission',)

class UserGroup(CreatedUpdated):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)

    class Meta:
        unique_together = ('user', 'group',)


    @property
    def group_name(self):
        return self.group.name

class GroupPermission(CreatedUpdated):
    group = models.ForeignKey(Group)
    permission = models.ForeignKey(Permission)

    class Meta:
        unique_together = ('group', 'permission',)
