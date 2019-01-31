from urllib import parse

import bugsnag as bugsnag
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from forgyft import settings
from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet, GiftFeedbackForm, ScraperInterestsForm, \
	UserForm, LoginForm, ExpertProfileForm
from forgyftapp.messaging import broadcast_to_slack, debug_log
from forgyftapp.models import GifteeProfile, GiftIdea
from forgyftapp.views import auth_views
from scraper.tasks import add


def experts_index(request):
	return render(request, "experts_homepage.html", {"page": "experts"})


def signup(request):
	return auth_views.signup(request, expert=True)

@login_required
def profile(request):
	user = request.user
	form = None

	if not user.expert_age or not user.expert_interests:
		if request.method == "POST":
			form = ExpertProfileForm(request.POST)

			if form.is_valid():
				age = form.cleaned_data.get("age")
				interests = form.cleaned_data.get("interests")


				user.expert_age = age
				user.expert_interests = interests
				user.save()
				return HttpResponseRedirect(request.path_info)

		else:
			form = ExpertProfileForm()


	return render(request, "experts/profile.html", {"page": "experts.profile", "expert_profile_form": form,
	                                                "sample_gift_request": True})