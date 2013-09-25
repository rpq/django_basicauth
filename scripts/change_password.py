#!/usr/bin/env python

if __name__ == '__main__':

    import os, sys
    PROJECT_DIRECTORY = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, PROJECT_DIRECTORY)

    from django.core.management import setup_environ
    from django_blog import settings

    setup_environ(settings)

    from basicauth import models

    u = models.User.objects.get(username=sys.argv[1])
    u.set_password(sys.argv[2])
    u.save()
