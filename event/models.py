from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django import forms
from account.models import Profile


class Czat(models.Model):
    autor=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="autor_czatu")
    uzytkownicy=models.ManyToManyField(Profile)
    name=models.CharField(max_length=255, null=True, default="czat")

class Zaproszenia(models.Model):
    autorr=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="autor_Zaproszenia")
    uzytkownicyy=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="Zaproszony",null=True)
    data=models.DateTimeField(auto_now=True)

    
class Wiadomosc(models.Model):
    autor=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="wiadomosci")
    tresc=models.TextField(max_length=255)
    data_utworzenia=models.DateTimeField(auto_now=True)
    czat=models.ForeignKey(Czat, on_delete=models.CASCADE)
    
class miejsce(models.Model):
    adres=models.CharField(max_length=100)
    miasto=models.CharField(max_length=100, default="Białystok")
    nazwa=models.CharField(max_length=100)
    zaakceptowane=models.BooleanField(default=False)
    Srednia_ocen=models.IntegerField( default=0)
    photo = models.ImageField(upload_to='miejsca/', blank=True, default='miejsca/Default.jpg')

    def __str__(self):
        return "{} ({}, {})".format(self.nazwa, self.adres, self.miasto)
        
    class Meta:
        verbose_name = 'Miejsce'
        verbose_name_plural = 'Miejsca'

class wydarzenie(models.Model):
    miejsce=models.ForeignKey(miejsce,on_delete=models.CASCADE)
    nazwa=models.CharField(max_length=50)
    data_rozpoczecia=models.DateField()
    organizator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wydarzenia')
    opis=models.TextField()
    uczestnicy=models.ManyToManyField(User,related_name="uczestnicy")
    photo = models.ImageField(upload_to="wydarzenia/", blank=True, default='miejsca/Default.jpg')
    def __str__(self):
        return self.nazwa

class komentarz_do_wydarzenia(models.Model):
    autor= models.ForeignKey(User,on_delete=models.CASCADE)
    wydarzenie=models.ForeignKey(wydarzenie,on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now=True)
    tresc=models.TextField()
    def __str__(self):
        return self.tresc

class komentarz_do_miejsca(models.Model):
    autor= models.ForeignKey(User,on_delete=models.CASCADE)
    miejsce=models.ForeignKey(miejsce,on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now=True)
    tresc=models.TextField()
    def __str__(self):
        return "%s"% {self.tresc}

class ogloszenie(models.Model):
    autor= models.ForeignKey(User,on_delete=models.CASCADE)
    tytul=models.CharField(max_length=20)
    data=models.DateTimeField(auto_now=True)
    zdjecie = models.ImageField(upload_to='ogloszenie/', blank=True, default='ogloszenie/Default.jpg')
    opis=models.TextField()
    def __str__(self):
        return self.tytul

class komentarz_do_ogloszenia(models.Model):
    autor= models.ForeignKey(User,on_delete=models.CASCADE)
    ogloszenie=models.ForeignKey(ogloszenie,on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now=True)
    tresc=models.TextField()
    def __str__(self):
        return "%s"% {self.tresc}

        
class Powiadomienie(models.Model):
    event = models.ForeignKey(wydarzenie,on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey(Czat,on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(User,on_delete=models.CASCADE)
    viewed = models.BooleanField()
    text = models.TextField()

class Ocena(models.Model):
    miejsce=models.ForeignKey(miejsce,on_delete=models.CASCADE,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    ocena=models.IntegerField()
    def __str__(self):
        return str(self.ocena)
        
class rate_user(models.Model):
    evaluative=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="evaluative")
    evaluated=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="evaluated")
    event=models.ForeignKey(wydarzenie, on_delete=models.CASCADE, related_name="event")
    
    
    
@receiver(post_save, sender=wydarzenie)
def hear_signal(sender, instance, **kwargs):
    print('hear_signal')
    add_notifications(instance)
    
    return

@receiver(post_save, sender=Wiadomosc)
def hear_signal_from_chat(sender, instance, **kwargs):
    print('hear_signal')
    add_notifications_from_chat(instance)
    
    return
    
def add_notifications(event_instance):
    print('add_notifications')
    for user in event_instance.uczestnicy.all():
        n = Powiadomienie(event=event_instance,
                        recipient=user,
                        viewed = False,
                        text = "Edytowano: {0}".format(event_instance.nazwa))
        n.save()
    return
    
   
def add_notifications_from_chat(message_instance):
    print('add_notifications_from_chat')
    for user in message_instance.czat.uzytkownicy.all():
        n = Powiadomienie(chat=message_instance.czat,
                        recipient=user.user,
                        viewed = False,
                        text = "Nowa wiadomość!: {0}".format(message_instance.czat.name))
        n.save()
    return
    

