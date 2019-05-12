from django import template
from datetime import datetime, timedelta
from django.template.defaulttags import register
from ..models import *
from django.utils import timezone
from account.models import Profile
from datetime import date
register = template.Library()


@register.filter
def is_friend(arg,user_id):
        tags=Profile.objects.get(pk=arg)
        
        for frend in tags.friends.all():
                if frend.user.id == user_id :
                        return False

        return True


@register.filter
def is_ok(wyrzenia,user):
        
        wydarzenia=wydarzenie.objects.get(pk=wyrzenia)
        Ocena = Ocena_wydarzenia.objects.filter(wydarzenie=wydarzenia,user=user)
        Data=wydarzenia.data_rozpoczecia
        today=date.today()
        wynik=today-Data

        if wynik.days >7:
                return True

        if Data>today:
                return True
        
        if not Ocena:
                 return False
       
        

        return True
        

 