from django.test import TestCase
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import Profile
import datetime


class WydarzenieTest(TestCase):
    def create_event(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        miejsce1 = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                          Srednia_ocen=2)
        wydarzenie1 = wydarzenie.objects.create(nazwa='WydarzenieTest', data_rozpoczecia=timezone.now(),
                                                opis="opis", miejsce=miejsce1, organizator=user)
        wydarzenie1.uczestnicy.add(user)
        return wydarzenie1

    def test_instance(self):
        wyd = self.create_event()
        self.assertTrue(isinstance(wyd, wydarzenie))

    def test_desription(self):
        wyd = self.create_event()
        self.assertEqual("opis", wyd.opis)

    def test_title(self):
        wyd = self.create_event()
        self.assertEqual(str(wyd), "WydarzenieTest")


class KomenatarzWydarzeniaTest(TestCase):
    def create_comment(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        miejsce1 = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                          Srednia_ocen=2)
        wydarzenie1 = wydarzenie.objects.create(nazwa='WydarzenieTest', data_rozpoczecia=timezone.now(),
                                                opis="opis", miejsce=miejsce1, organizator=user)
        wydarzenie1.uczestnicy.add(user)
        komentarz = komentarz_do_wydarzenia.objects.create(autor=user, tresc="komenatarz", data=timezone.now(),
                                                           wydarzenie=wydarzenie1)
        return komentarz

    def test_instance(self):
        komentarz = self.create_comment()
        self.assertTrue(isinstance(komentarz, komentarz_do_wydarzenia))

    def test_date(self):
        komentarz = self.create_comment()
        self.assertTrue(str(komentarz), "komentarz")

    def test_is_create_by_user(self):
        komentarz = self.create_comment()
        self.assertTrue(isinstance(komentarz.autor, User))


class KomentarzMiejsceTest(TestCase):
    def create_comment(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        miejsce1 = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=True,
                                          Srednia_ocen=2)
        komentarz = komentarz_do_miejsca.objects.create(tresc="tresc", autor=user, miejsce=miejsce1,
                                                        data=timezone.now())
        return komentarz

    def test_instance(self):
        kom = self.create_comment()
        self.assertTrue(kom, komentarz_do_miejsca)

    def test_place_accepted(self):
        print("place")
        kom = self.create_comment()
        self.assertIs(kom.miejsce.zaakceptowane, True)


class OgloszenieTest(TestCase):
    def create_adv(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        ogloszenie1 = ogloszenie.objects.create(autor=user, tytul="OgloszenieTest", data=timezone.now(), opis='opis')
        return ogloszenie1

    def test_instance(self):
        ogl = self.create_adv()
        self.assertTrue(isinstance(ogl, ogloszenie))

    def test_desription(self):
        ogl = self.create_adv()
        self.assertEqual("opis", ogl.opis)

    def test_title(self):
        ogl = self.create_adv()
        self.assertEqual(str(ogl), "OgloszenieTest")


class KomenatarzWydarzeniaTest(TestCase):
    def create_comment(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        ogloszenie1 = ogloszenie.objects.create(autor=user, tytul='tytul', data=timezone.now(), opis='opis')
        komentarz = komentarz_do_ogloszenia.objects.create(autor=user, ogloszenie=ogloszenie1, data=timezone.now(),
                                                           tresc="komenatarz")
        return komentarz

    def test_instance(self):
        komentarz = self.create_comment()
        self.assertTrue(isinstance(komentarz, komentarz_do_ogloszenia))

    def test_date(self):
        komentarz = self.create_comment()
        self.assertTrue(str(komentarz), "komentarz")

    def test_is_create_by_user(self):
        komentarz = self.create_comment()
        self.assertTrue(isinstance(komentarz.autor, User))


class OcenaTest(TestCase):
    def create_oc(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        miejsce1 = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                          Srednia_ocen=2)
        ocena = Ocena.objects.create(miejsce=miejsce1, user=user, ocena=5)
        return ocena

    def test_instance(self):
        oc = self.create_oc()
        self.assertTrue(isinstance(oc, Ocena))

    def test_ocena(self):
        oc = self.create_oc()
        self.assertEqual(str(oc), str(5))


# Sprint 8

class CzatTest(TestCase):
    def create_chat(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        user2 = User.objects.create_user("friend", "friend@example.com", "friend")
        friend = Profile.objects.create(user=user2, date_of_birth=datetime.datetime(1999, 3, 3))
        author = Profile.objects.create(user=user, date_of_birth=datetime.datetime(1997, 3, 3))
        chat = Czat.objects.create(autor=author, name="Nowy czat")
        chat.uzytkownicy.add(friend)
        return chat

    def test_name(self):
        chat = self.create_chat()
        self.assertEqual("Nowy czat", chat.name)

    def test_author(self):
        chat = self.create_chat()
        self.assertEqual(chat.autor.user.username, "user")

    def test_users_count(self):
        chat = self.create_chat()
        self.assertEqual(chat.uzytkownicy.count(), 1)


class ZaproszenieTest(TestCase):
    def create_invitation(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        user2 = User.objects.create_user("friend", "friend@example.com", "friend")
        friend = Profile.objects.create(user=user2, date_of_birth=datetime.datetime(1999, 3, 3))
        author = Profile.objects.create(user=user, date_of_birth=datetime.datetime(1997, 3, 3))
        invitation = Zaproszenia.objects.create(autorr=author, uzytkownicyy=friend)
        return invitation

    def test_author(self):
        invitation = self.create_invitation()
        self.assertEqual(invitation.autorr.user.username, "user")

    def test_invited(self):
        invitation = self.create_invitation()
        self.assertCountEqual(invitation.uzytkownicyy.user.username, "friend")

    def test_time(self):
        invitation = self.create_invitation()
        self.assertEqual(invitation.data.strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d'))


class WiadomoscTest(TestCase):
    def create_message(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        user2 = User.objects.create_user("friend", "friend@example.com", "friend")
        friend = Profile.objects.create(user=user2, date_of_birth=datetime.datetime(1999, 3, 3))
        author = Profile.objects.create(user=user, date_of_birth=datetime.datetime(1997, 3, 3))
        chat = Czat.objects.create(autor=author, name="Nowy czat")
        chat.uzytkownicy.add(friend)
        message = Wiadomosc.objects.create(autor=author, tresc="Witam wszystkich!", czat=chat)
        return message

    def test_message(self):
        message = self.create_message()
        self.assertEqual("Witam wszystkich!", message.tresc)
        self.assertEqual("user", message.autor.user.username)


class PowiadomienieTest(TestCase):
    def set_data(self):
        user = User.objects.create_user("user", "user1@example.com", "example")
        user2 = User.objects.create_user("friend", "friend@example.com", "friend")
        friend = Profile.objects.create(user=user2, date_of_birth=datetime.datetime(1999, 3, 3))
        author = Profile.objects.create(user=user, date_of_birth=datetime.datetime(1997, 3, 3))
        miejsce1 = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                          Srednia_ocen=2)
        wydarzenie1 = wydarzenie.objects.create(nazwa='WydarzenieTest', data_rozpoczecia=timezone.now(),
                                                opis="opis", miejsce=miejsce1, organizator=user)
        wydarzenie1.uczestnicy.add(user)
        wydarzenie1.uczestnicy.add(user2)
        chat = Czat.objects.create(autor=author, name="Nowy czat")
        chat.uzytkownicy.add(friend)
        add_notifications(wydarzenie1)
        Wiadomosc.objects.create(autor=author, tresc="Witam wszystkich!", czat=chat)

    def test_notification_for_event(self):
        self.set_data()
        notifications = Powiadomienie.objects.all()
        users = []
        notifications_users = []
        is_users_in_notifications = False
        for n in notifications:
            notifications_users.append(n.recipient)
        for u in Profile.objects.all():
            users.append(u.user)
        if all(u in users for u in notifications_users):
            is_users_in_notifications = True
        self.assertTrue(is_users_in_notifications)

    def test_notifications_context_for_event(self):
        self.set_data()
        notify = Powiadomienie.objects.all().first()
        event = notify.event
        self.assertEqual("Edytowano: {0}".format(event.nazwa), notify.text)

    def test_notifications_conetxt_for_chat(self):
        self.set_data()
        add_notifications_from_chat(Wiadomosc.objects.all().first())
        notify = Powiadomienie.objects.all().last()
        chat = notify.chat
        self.assertEqual("Nowa wiadomość!: {0}".format(chat.name), notify.text)

    def test_viewed(self):
        self.set_data()
        self.client.login(username="user", password="example")
        response = self.client.get('/notifications')
        self.assertNotEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'event/notifications.html')
        notifications = Powiadomienie.objects.all()
        is_viewed = False
        for n in notifications:
            if n.recipient.username == "user" and n.viewed:
                is_viewed = True
        self.assertTrue(is_viewed)


# Sprint 9

class RateUserTest(TestCase):
    def create_rate(self):
        evaluative = User.objects.create_user("evaluative", "evaluative@example.com", "evaluative")
        evaluated = User.objects.create_user("evaluated", "evaluated@example.com", "evaluated")
        user = User.objects.create_user("user", "user1@example.com", "example")
        evaluativeProfile = Profile.objects.create(user=evaluative, date_of_birth=datetime.datetime(1999, 3, 3))
        evaluatedProfile = Profile.objects.create(user=evaluated, date_of_birth=datetime.datetime(1999, 3, 3))
        place = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                       Srednia_ocen=2)
        event = wydarzenie.objects.create(nazwa='WydarzenieTest', data_rozpoczecia=timezone.now(),
                                          opis="opis", miejsce=place, organizator=user)
        rate = rate_user.objects.create(evaluative=evaluativeProfile, evaluated=evaluatedProfile, event=event)
        return rate

    def test_evaluative(self):
        rate = self.create_rate()
        self.assertEqual(rate.evaluative.user.email, "evaluative@example.com")

    def test_evaluated(self):
        rate = self.create_rate()
        self.assertEqual(rate.evaluated.user.email, "evaluated@example.com")

    def test_event(self):
        rate = self.create_rate()
        self.assertEqual(rate.event.nazwa, "WydarzenieTest")


class ViewsTest(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_load_my_friend(self):
        user = User.objects.create_user("user", "user@example.com", "user")
        Profile.objects.create(user=user, date_of_birth=datetime.datetime(1999, 3, 3))
        self.client.login(username='user', password='user')
        response = self.client.get('/account/my_friends')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/my_friends.html')

    def test_place_list_page(self):
        user = User.objects.create_user("user", "user@example.com", "user")
        Profile.objects.create(user=user, date_of_birth=datetime.datetime(1999, 3, 3))
        place = miejsce.objects.create(adres="adres", miasto="miasto", nazwa="nazwa", zaakceptowane=False,
                                       Srednia_ocen=2)
        self.client.login(username='user', password='user')
        response = self.client.get('/place-list')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['miejsca'], ['<miejsce: nazwa (adres, miasto)>'])

    def test_user_events_list(self):
        user = User.objects.create_user("user2", "user2@example.com", "user2")
        Profile.objects.create(user=user, date_of_birth=datetime.datetime(1999, 3, 3))
        WydarzenieTest.create_event(self)
        self.client.login(username='user2', password='user2')
        response = self.client.get('/moje_wydadzene')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['Wlasne'], [])
        self.assertQuerysetEqual(response.context['Udzial'], [])

    def test_user_events_list_2(self):
        user = User.objects.create_user("user2", "user2@example.com", "user2")
        Profile.objects.create(user=user, date_of_birth=datetime.datetime(1999, 3, 3))
        WydarzenieTest.create_event(self)
        self.client.login(username='user', password='example')
        response = self.client.get('/moje_wydadzene')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['Wlasne'], ['<wydarzenie: WydarzenieTest>'])
        self.assertQuerysetEqual(response.context['Udzial'], ['<wydarzenie: WydarzenieTest>'])

    def test_redirect_to_login(self):
        response = self.client.get('/moje_wydadzene')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/')

    def test_redirect_to_login(self):
        response = self.client.get('/notifications')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/account/login/')
    def test_event_detail(self):
        user = User.objects.create_user("user2", "user2@example.com", "user2")
        Profile.objects.create(user=user, date_of_birth=datetime.datetime(1999, 3, 3))
        event = WydarzenieTest.create_event(self)
        self.client.login(username='user2', password='user2')
        response = self.client.get('/events/{0}'.format(event.id))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['takePartButtonText'].split(" "),["'Wezmę'","'udział!'"])