from django.contrib import admin
from .models import *

admin.site.register(miejsce)
admin.site.register(wydarzenie)
admin.site.register(komentarz_do_wydarzenia)
admin.site.register(Powiadomienie)
admin.site.register(Ocena)
admin.site.register(Zaproszenia)