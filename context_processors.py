from basicauth import models

def logged_in_user(request):
    try:
        logged_in_user_id = request.session.get('logged_in_user_id')
        user = models.User.objects.get(pk=logged_in_user_id)
    except models.User.DoesNotExist:
        return {}
    d = {}
    d['logged_in_user'] = user
    return d
