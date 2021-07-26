from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.models import User
from django.conf import settings


# Create your views here.
def register(request):
	if request.method == 'POST':
		form =UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created you can now login!!!')
			return redirect('login')
	else:
		form =UserRegisterForm()


	return render(request, "users/register.html",{'form':form})
def login_user(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email=form.cleaned_data.get('email')
			password=form.cleaned_data.get('password')
			user=User.objects.filter(email=email).first()
			user = authenticate(username=user.username,password=password)
			login(request, user)
			messages.success(request, "Login successful")
			return redirect('blog-home')
		else:
			for field in form.errors:
				form[field].field.widget.attrs['class'] = 'invalid form-input' 
	else:
		form = LoginForm()
	return render(request, 'users/login.html',{'form':form})

def logout_user(request):
	logout(request)
	return redirect('login')
@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user,request=request)
		p_form = ProfileUpdateForm(request.POST,
									request.FILES,
									instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			user = User.objects.get(id=request.user.id)
			file_path = os.path.join(settings.BASE_DIR,user.profile.image.path)
			if p_form.cleaned_data.get('image') != user.profile.image:
				if not user.profile.image == 'default.jpeg':
					os.remove(file_path)
			u_form.save()
			p_form.save()
			if u_form.cleaned_data.get('is_active') == False:
				messages.warning(request, 'Your account has been deactivated')
				return redirect('login')
			else:
				messages.success(request, 'Your account has been updated')
				return redirect('profile')
	else:

		u_form = UserUpdateForm(instance=request.user,request=request)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
	'u_form':u_form,
	'p_form':p_form
	}
	return render(request, 'users/profile.html', context)

