from django.db import models
from django.http import HttpResponse
from django.utils import timezone

def json_redirect(redirect_url):
    return HttpResponse(
        simplejson.dumps({ 'redirect': redirect_url }),
        mimetype='application/json')

class CreatedUpdated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now())

    class Meta:
        abstract = True
