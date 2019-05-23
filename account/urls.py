"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('oauth/', include('social_django.urls', namespace='social')),
	path('logout/',views.Logout, name='logout'),
	path('register/', views.register, name='register'),
	path('edit/', views.edit_profile, name ='edit'),
	path('password-change/',auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'),name='password_change'),
	path('password-change-done/',auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),name='password_change_done'),
	path('password-reset/',auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html', html_email_template_name='account/password_reset_email.html', subject_template_name= 'account/sportcatch.txt'),name='password_reset_form'),
	path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
	path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),name='password_reset_complete'),
	path('password-reset-confirm/<uidb64>/<token>/$',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),name='password_reset_confirm'),
	path('account_info',views.account_info, name='my_account'),
	path('my_friends',views.my_friends, name='my_friends'),
	path('email/<slug:nick>',views.email,name='email'),
	path('account_info/<int:pk>',views.other_account_info,name='other_account_info'),
	path('incorrect_login/', views.user_login, name='incorrect_login'),
    path('delete_friend/<int:pk>',views.delete_friend, name='delete_friend'),
	path("regulamin/", views.regulamin, name="regulamin"),
    
	# <--
]
