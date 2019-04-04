from django import template

from django.template.defaulttags import register
from ..models import *
from account.models import Profile
register = template.Library()


@register.filter
def is_friend(arg,user_id):
        tags=Profile.objects.get(pk=arg)
        
        for frend in tags.friends.all():
                if frend.user.id == user_id :
                        return False

        return True