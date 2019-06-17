from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import *
from datetime import datetime


def get_all_logged_in_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=uid_list)

def logged_users(request):
    logged = get_all_logged_in_users()
    print("-------------------333333333333-------------------")
    print(logged)
    return {'zalogowani':len(logged),'request':request}

def registers_users(request):
    return {'zarejestrowani':Profile.objects.all().count(),'request':request}

def incoming_events(request):
    all_events = wydarzenie.objects.all()
    today = datetime.now().date()
    incoming = []
    for e in all_events:
        if(e.data_rozpoczecia > today):
            incoming.append(e)
    return{'nadchodzace':len(incoming),'request':request}