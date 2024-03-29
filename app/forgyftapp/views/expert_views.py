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
	UserForm, LoginForm, ExpertProfileForm, SampleGiftIdeaFormSet
from forgyftapp.messaging import broadcast_to_slack, debug_log
from forgyftapp.models import GifteeProfile, GiftIdea
from forgyftapp.views import auth_views
from scraper.tasks import add


def experts_index(request):
	return render(request, "experts_homepage.html", {"page": "experts"})


def signup(request):
	return auth_views.signup(request, expert=True)


@login_required
def expert_fulfill(request, slug):
	returnData = {}
	user = request.user

	gift_request = GifteeProfile.fromSlug(slug)

	if user != gift_request.expert:
		return redirect("forgyftapp:index")

	if request.method == "POST":
		gift_ideas = GiftIdeaFormSet(request.POST, instance=gift_request, prefix="gift_ideas")

		if "gift_ideas" in request.POST:
			if gift_ideas.is_valid():
				gift_ideas.save()

				published = (request.POST.get("published", 'false') == 'true')

				if published:
					if len(gift_request.ideas.all()) <= 0:
						return HttpResponseRedirect(reverse("forgyftapp:expert_fulfill", args=(slug,)))
					gift_request.submit(request)
				else:
					gift_request.unsubmit()

				return HttpResponseRedirect(reverse("forgyftapp:expert_fulfill", args=(slug,)))
	else:
		gift_ideas = GiftIdeaFormSet(instance=gift_request, prefix="gift_ideas")

	returnData["gift_ideas"] = gift_ideas


	returnData.update({"page": "experts.fulfill", "gift_request": gift_request})
	return render(request, "experts/fulfill.html", returnData)


@login_required
def profile(request):
	returnData = {}

	user = request.user
	if not user.is_expert:
		user.is_expert = True
		user.save()
	form = None
	sample_ideas_form = None
	sample_gift_request = None

	if not user.expert_age or not user.expert_interests:
		if request.method == "POST":
			form = ExpertProfileForm(request.POST)

			if form.is_valid():
				form.save(user)
				return HttpResponseRedirect(request.path_info)

		else:
			form = ExpertProfileForm()

		returnData["expert_profile_form"] = form
	else:
		sample_gift_request = user.expert_sample_gift_request
		if sample_gift_request.published:
			returnData["display_sample_request"] = False
			returnData["unfulfilled_requests"] = user.expert_request_set.filter(published=False).order_by('created')
			returnData["fulfilled_requests"] = user.expert_request_set.filter(published=True).order_by('created')
		else:
			returnData["display_sample_request"] = True
			if request.method == "POST":
				gift_ideas = SampleGiftIdeaFormSet(request.POST, instance=sample_gift_request, prefix="gift_ideas")

				if "gift_ideas" in request.POST:
					if gift_ideas.is_valid():
						gift_ideas.save()
						published = (request.POST.get("published", 'false') == 'true')

						if published:
							if len(sample_gift_request.ideas.all()) <= 0:
								return redirect("forgyftapp:expert_profile")
							sample_gift_request.submit()

						return redirect("forgyftapp:expert_profile")
			else:
				gift_ideas = SampleGiftIdeaFormSet(instance=sample_gift_request, prefix="gift_ideas")

			returnData["gift_ideas"] = gift_ideas

	returnData.update({"page": "experts.profile", "sample_gift_request": sample_gift_request})
	return render(request, "experts/profile.html", returnData)
