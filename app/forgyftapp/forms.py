from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from django import forms

from forgyftapp import models
from forgyftapp.models import GifteeProfile, User, GiftIdea, GiftFeedback
from forgyftapp.util.django_utils import get_client_ip


class GiftFeedbackForm(ModelForm):

	rating = forms.IntegerField(max_value=5, min_value=1, label="Rating", help_text="Please rate the gift ideas from "
	                                                                                "on a scale from 1 to 5.",
	                            required=True)
	feedback = forms.CharField(help_text="What did you think of the gift ideas, how can we improve in the future?",
	                           required=True, widget=forms.Textarea(attrs={"rows": "4"}))
	bought = forms.BooleanField(label="Bought", help_text="Did you buy one of the gift ideas?", required=False)

	def save(self, giftee_profile=None, commit=True):
		if not giftee_profile:
			raise TypeError("No giftee_profile object given to the GiftFeedbackForm.save method.")
		instance = super().save(commit=False)
		instance.giftee_profile = giftee_profile
		if commit:
			instance.save()
		return instance

	class Meta:
		model = GiftFeedback
		fields = ("rating", "feedback", "bought")


class GiftIdeaForm(ModelForm):

	idea = forms.CharField(widget=forms.Textarea(attrs={"rows": "2"}))
	explanation = forms.CharField(widget=forms.Textarea(attrs={"rows": "4"}))

	link = forms.CharField(widget=forms.Textarea(attrs={"rows": "2"}))
	image = forms.CharField(widget=forms.Textarea(attrs={"rows": "2"}), required=False)

	class Meta:
		model = GiftIdea
		fields = ("idea", "explanation", "link", "image", "published")

GiftIdeaFormSet = inlineformset_factory(GifteeProfile, GiftIdea, form=GiftIdeaForm, extra=1, can_delete=True)

class GifteeProfileForm(ModelForm):

	name = forms.CharField(max_length=150, help_text="What is the receiver's name?", required=True)
	gender = forms.ChoiceField(choices=models.gender.GENDER_CHOICES, help_text="What is the gender of the receiver?",
	                           required=True)
	age = forms.IntegerField(max_value=125, help_text="How old is the receiver of the gift?", required=True)
	relationship = forms.CharField(help_text="What is your relationship to the receiver? "
	                                         "Please be as specific as possible.", required=True)
	occasion = forms.CharField(help_text="What is the occasion that you will be giving the gift to the receiver?",
	                           required=True)
	price_upper = forms.IntegerField(max_value=10000, label="Max Price",
	                                 help_text="What is the most you are willing to spend on a gift? Please enter a number.", min_value=5)
	interests = forms.CharField(help_text="What are their main interests/hobbies, please be as specific as possible?",
	                            required=True, widget=forms.Textarea(attrs={"rows": "2"}))
	existing_related_items = forms.CharField(label="Items They Own",
	                                         help_text="What items do they already have that are"
	                                                   " related to their main interests/hobbies?")
	extra_info = forms.CharField(label="Special Information", help_text="Is there any other information you would like "
	                                                                    "us to know while finding the perfect gift?",
	                             required=False)

	def __init__(self, *args, **kwargs):
		account = kwargs.pop("account", False)
		super().__init__(*args, **kwargs)
		if not account:
			self.fields['email'] = forms.EmailField(label="Email Address",
		                              help_text="We'll shoot you an email when your results are "
		                                        "ready.", required=True)


	def save(self, user=None, request=None, commit=True):
		if not user and not self.fields.get("email", None):
			raise TypeError("No user object given to the GifteeProfileForm.save method.")
		if not request:
			raise TypeError("No request object given to the GifteeProfileForm.save method.")
		instance = super().save(commit=False)
		if not self.fields.get("email", None):
			instance.user = user
		else:
			instance.email = self.cleaned_data["email"]
		instance.ip_address = get_client_ip(request)
		if commit:
			instance.save()
		return instance

	class Meta:
		model = GifteeProfile
		fields = ("age", "gender", "relationship", "occasion", "price_upper",
		          "interests", "existing_related_items", "extra_info", "name")

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
	confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), min_length=6,
	                                   strip=False)
	class Meta:
		model = User
		fields = ("email", "password", "confirm_password", "first_name", "last_name")

	def save(self, commit=True, **kwargs):
		user = User(**{k: self.cleaned_data[k] for k in self.cleaned_data if k != "password" and k != "confirm_password"},
		            username=self.cleaned_data["email"])
		user.set_password(self.cleaned_data["password"])

		if commit:
			user.save()

		return user

	def clean_confirm_password(self):
		password1 = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("confirm_password")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Both passwords do not match.")
		return password2

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