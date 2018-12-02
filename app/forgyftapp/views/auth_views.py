from itertools import chain
from operator import attrgetter

from django.contrib.auth import login, authenticate, logout, backends
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from forgyftapp.forms import UserForm, LoginForm, ResetPasswordForm
from forgyftapp.messaging import debug_log
from forgyftapp.tokens import account_activation_token

from forgyftapp.models import User


def signup(request):
	redirectUrl = request.GET.get("next", None)

	if request.method == "POST":
		form = UserForm(request.POST)

		if form.is_valid():
			user = form.save()
			# user = form.save(commit=False)
			# user.is_active = False
			# user.save()
			#
			# current_site = get_current_site(request)
			# subject = "Activate your Forgyft Account"
			# message = render_to_string("auth/email/activation.html", {
			# 	"user": user,
			# 	"domain": current_site.domain,
			# 	"uid": force_text(urlsafe_base64_encode(force_bytes(user.pk))),
			# 	"token": account_activation_token.make_token(user),
			# })
			# user.email_user(subject, message)

			debug_log(f"New user signed up with email address \"{user.email}\", sent email to confirm address.")

			new_user = authenticate(request, username=form.cleaned_data["email"], password=form.cleaned_data["password"])
			login(request, new_user)
			if redirectUrl:
				return HttpResponseRedirect(redirectUrl)
			else:
				return HttpResponseRedirect(reverse("forgyftapp:index"))
	else:
		form = UserForm()

	return render(request, "auth/signup.html", {"form": form, "next": redirectUrl})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("forgyftapp:index"))

def login_view(request):
	redirectUrl = request.GET.get("next", None)
	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data.get("email")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=email, password=password)
			if user is not None:
				if not user.is_active:
					return render(request, "auth/login.html",
					              {"error": "The account that you are trying to log into has not confirmed their email yet.", "form": form})
				login(request, user)
				if redirectUrl:
					return HttpResponseRedirect(redirectUrl)
				else:
					return HttpResponseRedirect(reverse("forgyftapp:index"))
			else:
				return render(request,
				              "auth/login.html",
				              {"error": "The Email address or password entered does not match an account.", "form": form})
	else:
		form = LoginForm()

	return render(request, "auth/login.html", {"form": form, "next": redirectUrl})

def account_activation_sent(request):
	return render(request, "auth/activation_sent.html")


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_confirmed = True
		user.save()
		login(request, user, backend="django.contrib.auth.backends.ModelBackend")
		debug_log(f"User with email address \"{user.email}\" confirmed their email address.")
		return HttpResponseRedirect(reverse("forgyftapp:index"))
	else:
		return render(request, 'auth/activation_invalid.html')


def reset_password(request):
	return PasswordResetView.as_view(template_name="auth/reset/reset.html",
	                      email_template_name="auth/reset/reset_email.html",
	                      subject_template_name="auth/reset/reset_subject.txt",
	                      success_url=reverse("forgyftapp:reset_success"),
	                      from_email="Forgyft <support@forgyft.com>")(request) # TODO Name Change and Domain


def reset_confirm(request, uidb64=None, token=None):
	response = PasswordResetConfirmView.as_view(template_name='auth/reset/reset_confirm.html',
	                                  success_url=reverse('forgyftapp:reset_finished'),
	                                  form_class=ResetPasswordForm)(request, token=token, uidb64=uidb64)
	return response


def reset_success(request):
	return render(request, "auth/reset/reset_success.html")


def reset_finished(request):
	return render(request, "auth/reset/reset_finished.html")