from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from forgyftapp.models import GifteeProfile, User


class GiftIdeaForm(ModelForm):

	pass

class GifteeProfileForm(ModelForm):

	def save(self, user=None, commit=True):
		if not user:
			raise TypeError("No user object given to the ListingForm.save method.")
		instance = super().save(commit=False)
		instance.user = user
		if commit:
			instance.save()
		return instance

	class Meta:
		model = GifteeProfile
		fields = ("interests", )


class LoginForm(ModelForm):
	password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=6)

	# def clean_email(self):
	# 	email = self.cleaned_data["email"]
	# 	password = self.cleaned_data["password"]
	# 	user = authenticate(username=email, password=password)

	class Meta:
		model = User
		fields = ("email", "password")


class UserForm(ModelForm):
	# email = forms.EmailField(label="Email Address", widget=forms.EmailInput, u)
	first_name = forms.CharField(label="First Name", widget=forms.TextInput, required=True)
	last_name = forms.CharField(label="Last Name", widget=forms.TextInput, required=True)
	password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=6, strip=False)

	class Meta:
		model = User
		fields = ("email", "password", "first_name", "last_name")

	def save(self, commit=True, **kwargs):
		user = User(**{k: self.cleaned_data[k] for k in self.cleaned_data if k != "password"},
		            username=self.cleaned_data["email"])
		user.set_password(self.cleaned_data["password"])

		if commit:
			user.save()

		return user

	def clean_email(self):
		email = self.cleaned_data["email"]
		if User.objects.filter(email=email).exists():
			raise ValidationError("A User with that Email address already exists.")
		return email


# def createUser(self):
# 	if not self.is_valid():
# 		return
#
# 	email = self.cleaned_data["email"]
# 	first_name = self.cleaned_data["first_name"]
# 	last_name = self.cleaned_data["last_name"]
# 	password = self.cleaned_data["password"]
#
# 	User.objects.create_user(username=email,
# 	                         email=email,
# 	                         password=password,
# 	                         first_name=first_name,
# 	                         last_name=last_name)


class ResetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(
		label="New password",
		widget=forms.PasswordInput,
		strip=False,
		min_length=6
	)
	new_password2 = forms.CharField(
		label="New password confirmation",
		strip=False,
		widget=forms.PasswordInput,
		min_length=6
	)

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
				)
		return password2