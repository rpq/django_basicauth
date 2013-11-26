#!/usr/bin/env python

if __name__ == '__main__':

    import os, sys
    PROJECT_DIRECTORY = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, PROJECT_DIRECTORY)

    PROJECT_DIR_NAME = os.path.basename(PROJECT_DIRECTORY)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
        '{}.settings'.format(PROJECT_DIR_NAME))

    from basicauth import models

    u = models.User(username=sys.argv[1], email=sys.argv[3])
    u.set_password(sys.argv[2])
    u.save()
