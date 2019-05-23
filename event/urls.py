from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('events', views.events_list, name='events_list'),
    path('events/<int:pk>', views.event_detail, name='event_detail'),
    path('editevents/<int:pk>', views.event_edit, name='event_edit'),
    path('events/<int:pk>/edit', views.WydarzenieUpdateView.as_view(), name='edit_event'),
    path('', views.index, name='index'),
    path('add', views.WydarzenieCreateView.as_view(), name='new_event'),
    path('events/new_adv', views.OgloszenieCreateView.as_view(), name='new_adv'),
    path('take_part/<int:event_id>/', views.take_part, name='take_part'),
    path('notifications', views.get_notifications, name='get_notifications'),
    path('new_chat', views.new_chat, name='new_chat'),
    path('chats', views.show_my_chats, name='chats'),
    path('chat/<int:pk_chat>', views.concrete_chat, name='concrete_chat'),
    path('create-new-place', views.MiejsceCreateView.as_view(), name="new_place"),
    path('success/<int:pk>', views.success_info, name='success_info'),
    path('place-list', views.ListaMiejsc, name='place_list'),
    path('place/<int:pk>/', views.Miejsce_wydarzenia, name='miejsce_wydarzenia'),
    path('deleteCom/<int:pk>/<int:comPK>/', views.Delete_Com, name='delete_com'),
    path('deleteCom2/<int:pk>/<int:comPK>/', views.Delete_Com2, name='delete_com2'),
    path('place/edit/<int:pk>', views.Edite_place, name='Edite_place'),
    path('deletePlace/<int:pk>', views.Delete_place, name='Delete_place'),
    path('accept/<int:pk>', views.Accept, name='Accept'),
    path('Edit/Comment/<int:miejscePK>/<int:pk>', views.EditComment, name='EditComment'),
    path("moje_wydadzene", views.get_self_events, name="moje_wydzarzenia"),
    path("event_delete/<int:pk>", views.event_delet, name="event_delete"),
    path("usun_uczestnika/<int:pk>/<int:ucz>", views.uczestnik_delete, name="usun_uczestnika"),
    path("events/adv_list", views.AdvList, name='advlist'),
    path("events/adv/<int:pk>", views.adv_detail, name='adv_detail'),
    path('events/adv/<int:pk>/edit', views.adv_edit, name='adv_edit'),
    path('deleteCom3/<int:pk>/<int:comPK>/', views.Delete_Com3, name='delete_com3'),
    path('deleteAdv/<int:pk>',views.Delete_adv,name='adv_delete'),
    path('events/adv/<int:pkadv>/<int:pk>',views.EditCommentAdv,name='EditCommentAdv'),
    path("searching/",views.searching,name="searching"),
    path('Ocena/<int:ocena>/<int:pkmiast>',views.Ocenki,name='Ocena'),
    path('Ocena_w/<int:ocena>/<int:pkwydarzeni>',views.Ocenki_w,name='Ocena_w'),
    path("authors/", views.authors, name="authors"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
