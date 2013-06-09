import hashlib

from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

def json_redirect(redirect_url):
    return HttpResponse(
        simplejson.dumps({ 'redirect': redirect_url }),
        mimetype='application/json')

class CreatedUpdated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now())

    class Meta:
        abstract = True

from django.core.mail import EmailMultiAlternatives

class DjangoTemplate(object):

    def __init__(self, **kwargs):
        self.template_dictionary = kwargs.pop('template_dictionary')
        self.template_location = kwargs.pop('template_location')

    def get_string(self):
        return get_template(self.template_location).render(
            Context(self.template_dictionary))

class VerifyRegistrationEmail(object):
    EMAIL_SUBJECT = 'Verify your e-mail'
    EMAIL_TEMPLATE_LOCATION_PLAINTEXT = 'basicauth/emails/verify_registration.txt'
    EMAIL_TEMPLATE_LOCATION_HTML = 'basicauth/emails/verify_registration.html'
    EMAIL_FROM = 'rpq@winscores.com'

    @classmethod
    def get_plaintext(self, d):
        self.EMAIL_TEMPLATE_LOCATION

    @classmethod
    def get_html(self, d):
        return DjangoTemplate(
            template_location=self.EMAIL_TEMPLATE_LOCATION_HTML,
            template_dictionary=d).get_string()

    @classmethod
    def get_plaintext(self, d):
        return DjangoTemplate(
            template_location=self.EMAIL_TEMPLATE_LOCATION_PLAINTEXT,
            template_dictionary=d).get_string()

class Registration(models.Model):

    verify_id = models.TextField(null=False, blank=False)
    verified = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        abstract = True

    def send_verify_email(self):
        self.verify_id = self.create_verify_id()
        self.save()

        d = {
            'host': settings.ROOT_HOST_URL,
            'user': self,
            'link': '{0}{1}'.format(
                settings.ROOT_HOST_URL,
                reverse('register_email_verify', args=[self.verify_id,]))
        }

        msg = EmailMultiAlternatives(
            VerifyRegistrationEmail.EMAIL_SUBJECT,
            VerifyRegistrationEmail.get_plaintext(d),
            VerifyRegistrationEmail.EMAIL_FROM,
            [self.email])
        msg.attach_alternative(
            VerifyRegistrationEmail.get_html(d),
            'text/html')
        msg.send()

    def create_verify_id(self):
        h = hashlib.new('sha512')
        h.update(
            timezone.now().strftime('%Y%m%d%H%M%s') + self.email)
        return h.hexdigest()

    def verify(self):
        self.verified = True
