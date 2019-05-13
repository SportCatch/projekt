from datetime import datetime
from account.models import Profile
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import Library
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from datetime import date
register = Library()

info = ["Twoje ogłoszenie zostało utworzone.",
        "Twoje wydarzenie zostało utworzone.",
        "Czeka na akceptację administratora."]




class OgloszenieCreateView(CreateView):
    profiles = Profile.objects.all()
    model = ogloszenie
    form_class = ogloszenieForm
    success_url = reverse_lazy('success_info', kwargs={'pk': 0})

    def form_valid(self, form):
        ogloszenie = form.save(commit=False)
        ogloszenie.autor = self.request.user
        ogloszenie.save()
        return super().form_valid(form)



class WydarzenieCreateView(CreateView):
    profiles = Profile.objects.all()
    model = wydarzenie
    form_class = wydarzenieForm
    success_url = reverse_lazy('success_info', kwargs={'pk': 1})

    def form_valid(self, form):
        data = form.cleaned_data.get("data_rozpoczecia")
        print(data)
        new_wydarzenie = form.save(commit=False)
        new_wydarzenie.organizator = self.request.user
        new_wydarzenie.save()
        return super().form_valid(form)


class MiejsceCreateView(CreateView):
    profiles = Profile.objects.all()
    model = miejsce
    form_class = miejsceForm
    success_url = reverse_lazy('success_info', kwargs={'pk': 2})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WydarzenieUpdateView(UpdateView):
    model = wydarzenie
    fields = ('nazwa', 'opis', 'miejsce', 'data_rozpoczecia', 'uczestnicy')
    template_name = 'event/edit_event.html'
    # pk_url_kwarg = 'pk'
    context_object_name = 'wydarzenie'

    def form_valid(self, form):
        wydarzenie = form.save(commit=False)
        wydarzenie.organizator = self.request.user
        wydarzenie.save()
        return redirect('event_detail', pk=wydarzenie.pk)


@register.filter
def is_false(arg):
    if (arg != "/account/login/"):
        return arg is True
    return arg is False


def index(request):
    profiles = Profile.objects.all()
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
        request.session['sprawdz'] = Sprawdz(request)
        request.session['new_notifications'] = get_amount_of_unviewed_notifications(request)

    return render(request, 'index.html', {'profiles': profiles, 'user': user})


def events_list(request):
    user = Profile.objects.all()
    profiles = Profile.objects.all()
    events = wydarzenie.objects.order_by('data_rozpoczecia')
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    return render(request, 'event/events_list.html', {'events': events, 'profiles': profiles, 'user': user})


def Sprawdz(request):
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
        id = request.user
        Udzial = wydarzenie.objects.filter(uczestnicy=id)
        for wyd in Udzial:
            Data=wyd.data_rozpoczecia
            today=date.today()
            wynik=today-Data
            if wynik.days ==-1:
                pow=Powiadomienie()
                pow.event=wyd
                pow.recipient=request.user
                pow.text="Za niedlugo masz wydarzenie:\n "+wyd.nazwa+" Odbedzie sie \n"+wyd.data_rozpoczecia.strftime("%Y-%m-%d %H:%M:%S")
                pow.viewed=True
                pow.save()
            if wynik.days==0:
                pow=Powiadomienie()
                pow.recipient=request.user
                pow.text="Dzisaj masz wydarzenie \n"+wyd.nazwa+" Odbedzie sie \n"+wyd.data_rozpoczecia.strftime("%Y-%m-%d %H:%M:%S")
                pow.viewed=True
                pow.save()


def event_delet(request, pk):
    event = get_object_or_404(wydarzenie, pk=pk)
    event.delete()

    return redirect('moje_wydzarzenia')


def uczestnik_delete(regest, pk, ucz):
    event = get_object_or_404(wydarzenie, pk=pk)
    ucze = event.uczestnicy
    w = ucze.objects.generic(id=ucz)
    w.delete()
    return redirect('editevents', pk=pk)


def adv_edit(request, pk):
    user = Profile.objects.all()
    adv = get_object_or_404(ogloszenie, pk=pk)
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    if request.method == "POST":
        form = ogloszenieForm(instance=adv, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('advlist', {'user': user})
    else:
        form = ogloszenieForm(instance=adv)
    context = {'uform': form, 'user': user}
    return render(request, 'event/adv_edit.html', context)


def event_edit(request, pk):
    user = Profile.objects.all()
    event = get_object_or_404(wydarzenie, pk=pk)
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    ilosc = len(event.uczestnicy.all())
    if request.user == event.organizator:
        if request.method == "POST":
            form = WydarzenieForm(instance=event, data=request.POST)

            if form.is_valid():
                form.save()
                return redirect('moje_wydzarzenia', {'user': user})

        else:
            form = WydarzenieForm(instance=event)

    contex = {'Wydarzenie': event, 'uform': form, 'ilosc': ilosc, 'user': user}
    return render(request, 'event/event_edit.html', contex)


def adv_detail(request, pk):
    user = Profile.objects.all()
    adv = get_object_or_404(ogloszenie, pk=pk)
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    komentarze = komentarz_do_ogloszenia.objects.all()
    komentarz_form = None
    czy_nowy_komentarz = False
    if request.method == 'POST':
        komentarz_form = komentarzOgloszenieForm(data=request.POST)
        if komentarz_form.is_valid():
            nowy_komentarz = komentarz_form.save(commit=False)
            nowy_komentarz.ogloszenie = adv;
            nowy_komentarz.autor = request.user
            nowy_komentarz.save()
            czy_nowy_komentarz = True
        else:
            komentarz_form = komentarzOgloszenieForm()

    return render(request, 'event/adv_detail.html',
                  {'flag': czy_nowy_komentarz, 'adv': adv, 'komentarze': komentarze, 'komentarz_form': komentarz_form,
                   'user': user})


def event_detail(request, pk):
    user = Profile.objects.all()
    event = get_object_or_404(wydarzenie, pk=pk)
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    uczestnicy = event.uczestnicy.all()
    komentarze = komentarz_do_wydarzenia.objects.filter(wydarzenie=event.id)
    komentarz_form = None
    czy_nowy_komentarz = False
    if request.method == 'POST':
        komentarz_form = komentarzWydarzeniaForm(data=request.POST)
        if komentarz_form.is_valid():
            nowy_komentarz = komentarz_form.save(commit=False)
            nowy_komentarz.wydarzenie = event
            nowy_komentarz.autor = request.user
            nowy_komentarz.save()
            czy_nowy_komentarz = True
        else:
            komentarz_form = komentarzWydarzeniaForm()

    if not (request.user in event.uczestnicy.all()):
        takePartButtonText = "Wezmę udział!"
    else:
        takePartButtonText = "Jednak nie wezmę udziału"

    return render(request, 'event/event_detail.html', {'flag': czy_nowy_komentarz,
                                                       'event': event, 'uczestnicy': uczestnicy,
                                                       'komentarze': komentarze,
                                                       'komentarz_form': komentarz_form,
                                                       'takePartButtonText': takePartButtonText, 'user': user})


def take_part(request, event_id):
    '''Dodanie (lub wypisanie) użytkownika z wydarzenia.'''
    event = wydarzenie.objects.get(id=event_id)
    if not request.user in event.uczestnicy.all():
        event.uczestnicy.add(request.user)
    else:
        event.uczestnicy.remove(request.user)

    return HttpResponseRedirect(reverse('event_detail',
                                        args=[event_id]))


def get_notifications(request):
    '''Wyświetlenie wszystkich powiadomień dla danego użytkownika.'''

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    notifications = Powiadomienie.objects.all().filter(recipient=request.user)
    print(str(len(notifications)))
    for notification in notifications:
        notification.viewed = True
        notification.save()
    try:
        user = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user = None
    notifications = Powiadomienie.objects.all().filter(recipient=request.user)
    context = {'notifications': notifications, 'user': user}
    return render(request, 'event/notifications.html', context)


def get_amount_of_unviewed_notifications(request):
    notifications = Powiadomienie.objects.all().filter(recipient=request.user, viewed=False)
    return "Powiadomienia ({0})".format(str(len(notifications)))


def get_self_events(request):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
        id = request.user
        Wlasne = wydarzenie.objects.filter(organizator=id)
        Udzial = wydarzenie.objects.filter(uczestnicy=id)



        context = {'Wlasne': Wlasne, 'Udzial': Udzial, 'user': user,'userr':id}
        return render(request, 'event/moje_wydarzenia.html', context)
    return redirect('login')


def show_my_chats(request):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        chats = Czat.objects.filter(autor__user=request.user)
        logged_user_profile = Profile.objects.get(user=request.user)
        other_chats = []
        for czat in Czat.objects.all():
            if logged_user_profile in czat.uzytkownicy.all():
                other_chats.append(czat)

        print(str(len(chats)))
        context = {'chats': chats, 'other_chats': other_chats, 'user': user}
        return render(request, "event/chats.html", context)
    return redirect('login')


def make_name(profiles):
    name = ''
    for profile in profiles:
        name += profile.user.username
        name += ', '

    return name[0:-2]


def new_chat(request):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form = CzatForm(request.user, request.POST)
            if form.is_valid():
                users = form.cleaned_data['choices']
                czat = Czat(name=make_name(users), autor=Profile.objects.get(user=request.user))
                czat.save()
                for user in users:
                    czat.uzytkownicy.add(user)
                return HttpResponseRedirect(reverse('concrete_chat',
                                                    args=[czat.id]))

                czat.save()
        form = CzatForm(request.user)
        context = {'form': form, 'user': user}
        return render(request, "event/new_chat.html", context)
    return redirect('login')


def concrete_chat(request, pk_chat):
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
    czat = Czat.objects.get(id=pk_chat)
    if not ((request.user not in czat.uzytkownicy.all()) or (request.user != czat.autor.user)):
        return HttpResponseRedirect(reverse('new_chat', {'user': user}))

    if request.method == 'POST':
        form = WiadomoscForm(request.POST)
        if form.is_valid():
            message_tresc = form.cleaned_data['tresc']
            message = Wiadomosc(autor=Profile.objects.get(user=request.user),
                                tresc=message_tresc,
                                czat=Czat.objects.get(id=pk_chat))
            message.save()

    messages = Wiadomosc.objects.filter(czat__id=pk_chat)
    form = WiadomoscForm()
    context = {'form': form, 'messages': messages, 'user': user}
    return render(request, "event/concrete_chat.html", context)


def success_info(request, pk):
    user = Profile.objects.all()
    if not request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
        return reverse_lazy('index')

    context = {'info': info[pk], 'user': user}
    return render(request, "success_info.html", context)


def ListaMiejsc(request):
    user = Profile.objects.all()

    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None

    miejsca_lista = miejsce.objects.all()
    profiles = Profile.objects.all()

    return render(request, 'event/place_list.html', {'miejsca': miejsca_lista, 'profiles': profiles, 'user': user})


def Ocenki(request, ocena, pkmiast):
    oceniane = miejsce.objects.get(pk=pkmiast)
    user = request.user
    Spraw = Ocena.objects.filter(user=user, miejsce=oceniane)
    if not Spraw:
        nowa = Ocena()
        nowa.miejsce = oceniane
        nowa.user = user
        nowa.ocena = ocena
        nowa.save()
        Srednia = Ocena.objects.filter(miejsce=oceniane)
        srednia = 0
        ile = 0
        for a in Srednia:
            srednia = srednia + a.ocena
            ile = ile + 1
        oceniane.Srednia_ocen = srednia / ile
        oceniane.save()

    return HttpResponseRedirect(reverse('place_list'))



def Ocenki_w(request, ocena, pkwydarzeni):
    oceniane = wydarzenie.objects.get(pk=pkwydarzeni)
    user = request.user
    Spraw = Ocena_wydarzenia.objects.filter(user=user, wydarzenie=oceniane)
    if not Spraw:
        nowa = Ocena_wydarzenia()
        nowa.wydarzenie = oceniane
        nowa.user = user
        nowa.ocena = ocena
        nowa.save()
        Srednia = Ocena_wydarzenia.objects.filter(wydarzenie=oceniane)
        srednia = 0
        ile = 0
        for a in Srednia:
            srednia = srednia + a.ocena
            ile = ile + 1
        oceniane.Srednia_ocen = srednia / ile
        oceniane.save()

    return HttpResponseRedirect(reverse('place_list'))



def Miejsce_wydarzenia(request, pk):
    user = Profile.objects.all()
    nasze_miejsce = miejsce.objects.get(pk=pk)
    events = wydarzenie.objects.all().filter(miejsce=nasze_miejsce)
    czy_oceniny = False
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
        ocena = Ocena.objects.filter(user=request.user)

        for pom in ocena:
            if pom.miejsce == nasze_miejsce:
                czy_oceniny = True

    komentarze = komentarz_do_miejsca.objects.filter(miejsce=nasze_miejsce).order_by('-data')
    komentarz_form = None
    ilosc = len(events)
    czy_nowy = False
    if request.method == 'POST':
        komentarz_form = komentarzeMiejscaForm(data=request.POST)
        if komentarz_form.is_valid():
            nowy_komentarz = komentarz_form.save(commit=False)
            nowy_komentarz.miejsce = nasze_miejsce
            nowy_komentarz.autor = request.user
            nowy_komentarz.save()
            czy_nowy = True
        else:
            komentarz_form = komentarzeMiejscaForm()
    return render(request, 'event/miejsce_eventy.html', {'events': events,
                                                         'nasze_miejsce': nasze_miejsce,
                                                         'ilosc': ilosc,
                                                         'komentarze': komentarze,
                                                         'komentarz_form': komentarz_form,
                                                         'czy_nowy': czy_nowy,
                                                         'Ocenione_m': czy_oceniny,
                                                         'user': user
                                                         })


def Delete_Com(request, pk, comPK):
    nasze_miejsce = miejsce.objects.get(pk=pk)
    d = komentarz_do_miejsca.objects.get(miejsce=nasze_miejsce, pk=comPK)
    d.delete()
    return redirect('miejsce_wydarzenia', pk=pk)


def Delete_Com2(request, pk, comPK):
    nasze_wydarzenie = wydarzenie.objects.get(pk=pk)
    d = komentarz_do_wydarzenia.objects.get(wydarzenie=nasze_wydarzenie, pk=comPK)
    d.delete()
    return redirect('event_detail', pk=pk)


def Delete_Com3(reqest, pk, comPK):
    nasze_komentarze = ogloszenie.objects.get(pk=pk)
    d = komentarz_do_ogloszenia.objects.get(ogloszenie=nasze_komentarze, pk=comPK)
    d.delete()
    return redirect('adv_detail', pk=pk)


def Edite_place(request, pk):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    a = miejsce.objects.get(pk=pk)
    if request.method == 'POST':
        miejsce_form = miejsceEditForm(instance=a, data=request.POST)
        if miejsce_form.is_valid():
            miejsce_form.save()
            return redirect('place_list')
    else:
        miejsce_form = miejsceEditForm(instance=a)
    context = {'miejsce_form': miejsce_form, 'miejsce': a.nazwa}
    return render(request, 'event/edytuj_miejsce.html', context)


def Delete_place(self, pk):
    nasze_miejsce = miejsce.objects.get(pk=pk)
    nasze_miejsce.delete()
    return redirect('place_list')


def Delete_adv(self, pk):
    adv = ogloszenie.objects.get(pk=pk)
    adv.delete()
    return redirect('advlist')


def Accept(self, pk):
    nasze_miejsce = miejsce.objects.get(pk=pk)
    nasze_miejsce.zaakceptowane = True
    nasze_miejsce.save()
    return redirect('place_list')


def EditComment(request, pk, miejscePK):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    komentarz = komentarz_do_miejsca.objects.get(pk=pk)
    if request.method == 'GET':
        komentarz_form = CommentEditForm(instance=komentarz, data=request.POST)
        if komentarz_form.is_valid():
            komentarz_form.save()
            return redirect('miejsce_wydarzenia', pk=miejscePK)
        else:
            komentarz_form = CommentEditForm(instance=komentarz)
    if request.method == 'POST':
        komentarz_form = CommentEditForm(instance=komentarz, data=request.POST)
        komentarz_form.save()
        return redirect('miejsce_wydarzenia', pk=miejscePK)
    context = {'form': komentarz_form, 'user': user}
    return render(request, 'event/edit_comment.html', context)


def EditCommentAdv(request, pk, pkadv):
    komentarz = komentarz_do_ogloszenia.objects.get(pk=pk)
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    if request.method == 'GET':
        komentarz_form = CommentEditForm(instance=komentarz, data=request.POST)
        if komentarz_form.is_valid():
            komentarz_form.save()
            return redirect('adv_detail', pk=pkadv)
        else:
            komentarz_form = CommentEditForm(instance=komentarz)
    if request.method == 'POST':
        komentarz_form = CommentEditForm(instance=komentarz, data=request.POST)
        komentarz_form.save()
        return redirect('adv_detail', pk=pkadv)
    context = {'form': komentarz_form, 'user': user}
    return render(request, 'event/edit_comment.html', context)


def AdvList(request):
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    lista = ogloszenie.objects.all()
    return render(request, 'event/adv_list.html', {'lista': lista, 'user': user})


def searching(request):
    users = None
    events = None
    places = None
    user = Profile.objects.all()
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    if request.method == 'GET':
        search_phrase = request.GET.get("search_phrase", None)
        choice = request.GET.get("wybor", None)
        if choice == 'event':
            events = wydarzenie.objects.filter(nazwa__icontains=search_phrase)
            return render(request, 'event/search.html',
                          {'events': events, 'users': users, 'places': places, 'user': user})
        if choice == 'place':
            places = miejsce.objects.filter(nazwa__icontains=search_phrase)
            return render(request, 'event/search.html',
                          {'events': events, 'users': users, 'places': places, 'user': user})
        if choice == 'person':
            users = User.objects.filter(username__icontains=search_phrase)
            return render(request, 'event/search.html',
                          {'events': events, 'users': users, 'places': places, 'user': user})
        return render(request, 'event/search.html', {'events': None, 'users': None, 'places': None, 'user': user})

def authors(request):
    return render(request,'event/authors.html',{})