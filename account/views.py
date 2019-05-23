from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm,UserRegistrationForm, UserEditForm, EditProfieForm, ContactForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User

profiles = Profile.objects.all()
def user_login(request):
	next = request.POST.get('next', '/')
	if request.method =='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/')
				else:
					return HttpResponse('Konto zostało zablokowane')
			else:

				return render(request, 'account/incorrect_login.html', {'form': form})
	else:
		form = LoginForm()

	return render(request, 'account/login.html', {'form': form})
	

@login_required
def home(request):
    return render(request, 'core/home.html',{'profiles':profiles})
	
def Logout(request):
	logout(request)
	return redirect('/')

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			return redirect('/account/login')
	else:
		user_form = UserRegistrationForm()
	return render(request,'account/register.html',{'user_form': user_form})


@login_required
def edit_profile(request):
	"""Edytowanie profilu użytkownika."""
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = EditProfieForm(instance=request.user.profile,
									   data=request.POST,
									   files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = EditProfieForm(instance=request.user.profile)


	context = {'user_form': user_form, 'profile_form': profile_form,'profiles':profiles}
	return render(request, 'account/edit_profile.html', context)

def account_info(request):
	profil = Profile.objects.get(user=request.user)
	return render(request, 'account/account_info.html', {'user': profil})

def other_account_info(request, pk):
	u = User.objects.get(pk=pk)
	user = Profile.objects.get(user=u)
	return render(request, 'account/account_info.html', {'user': user})

def my_friends(request):
	profil = Profile.objects.get(user=request.user)
	return render(request, 'account/my_friends.html',{'user':profil})

def email(request, nick):
    if request.method == 'GET':
        form = ContactForm()
    else:
        to_user = User.objects.get(username= nick)
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            to_email = (to_user.email,"")
            try:
                send_mail(subject, message, "test.django34@gmail.com", to_email)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    return render(request, "account/email.html", {'form': form})

def delete_friend(request, pk):
    actual_user = Profile.objects.get(user = request.user)
    friend_user = User.objects.get(pk = pk)
    deleted_friend = Profile.objects.get(user = friend_user)
    actual_user.friends.remove(deleted_friend)
    deleted_friend.friends.remove(actual_user)
    return render(request, 'account/my_friends.html',{'user':actual_user})
    
def regulamin(request):
    return render(request, 'account/regulamin.html', {})