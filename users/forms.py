from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from.models import Profile


class UserRegisterForm(UserCreationForm):

	email = forms.EmailField(widget=forms.EmailInput)
	password1 = forms.CharField(widget=forms.PasswordInput,label='password')
	password2 = forms.CharField(widget=forms.PasswordInput,label='password confirmation')

	def clean_email(self):
		email = self.cleaned_data.get('email')

		user = User.objects.filter(email=email).first()
		# print(user)
		if user:
			raise forms.ValidationError('This email is already taken!! try with another one')
		return email


	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		help_texts = {
		'username':None,
		'email':None,
		'password1':None,
		}

class LoginForm(forms.Form):
	email = forms.EmailField(
		label='Email',
		max_length=100,
		widget=forms.EmailInput(attrs={'class':'form-input','placeholder':' '}))
	password = forms.CharField(label='Password',
		min_length=8,
		widget=forms.PasswordInput(attrs={'class':'form-input','placeholder':' '}))

	def clean(self):
		cleaned_data= super().clean()
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		user = User.objects.filter(email = email).first()

		if user:
			if not user.check_password(password):
				raise forms.ValidationError({'password':'Invalid password'})
			if not user.is_active:
				raise forms.ValidationError({'email':'Your account has been deactivated.'})
		else:
			raise forms.ValidationError({'email':'There is no user with this email'})
	
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(required=True,widget=forms.EmailInput(),label='Email address')

	def __init__(self, *args, **kwargs):
		self.request =kwargs.pop('request')
		super(UserUpdateForm, self).__init__(*args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email != self.request.user.email:
			user = User.objects.filter(email=email).first()
			if user:
				raise forms.ValidationError("A user with that email already exists.")
		return email


	class Meta:
		model = User
		fields = ['username','email','is_active']

		help_texts = {
		'is_active':'Unselect this to deactivate your account',
		'username':None
		}




class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']
