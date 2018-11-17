from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet
from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.models import GifteeProfile, GiftIdea


def index(request):
	return render(request, "homepage.html", {"page": "home"})

def terms(request):
	return render(request, "static/terms.html")

def about(request):
	return render(request, "static/about.html", {"page": "about"})

def privacy(request):
	return render(request, "static/privacy.html")

@login_required
def gift_request(request, profile=None):
	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if not giftee_profile.published:
			return redirect("forgyftapp:request")

		return render(request, "request.html", {"giftee_profile": giftee_profile,
		                                        "ideas": GiftIdea.objects.filter(giftee_profile=giftee_profile),
		                                        "page": "request"})
	else:
		giftee_profiles = GifteeProfile.objects.filter(user=request.user)

		return render(request, "request.html", {"giftee_profiles": giftee_profiles, "page": "request"})

def gift_form(request):
	if request.method == "POST":
		form = GifteeProfileForm(request.POST)
		if form.is_valid():
			form.save(user=request.user)
			return redirect("forgyftapp:index")
	else:
		form = GifteeProfileForm()

	return render(request, "gift_form.html", {"form": form, "page": "request"})


@staff_member_required
def fulfill(request, profile=None):
	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if request.method == "POST":
			gift_ideas = GiftIdeaFormSet(request.POST, instance=giftee_profile)
			i = 0
			for form in gift_ideas:
				if len(form.changed_data) == 1 and form.changed_data[0] == "published":
					form.changed_data = []
				i += 1
			if gift_ideas.is_valid():
				gift_ideas.save()

				published = False
				for form in gift_ideas:
					if len(gift_ideas.forms[0].cleaned_data) > 0 and gift_ideas.forms[0].cleaned_data["published"]:
						published = True

				if published:
					giftee_profile.submit(request)
				else:
					giftee_profile.unsubmit()
		else:
			gift_ideas = GiftIdeaFormSet(instance=giftee_profile)

		published = giftee_profile.published or (hasattr(gift_ideas.forms[0], "cleaned_data") and gift_ideas.forms[0].cleaned_data["published"])

		return render(request, "fulfill.html", {"giftee_profile": giftee_profile, "gift_ideas": gift_ideas,
		                                        "page": "fulfill", "published": published})
	else:
		giftee_profiles_unpublished = GifteeProfile.objects.filter(published=False)
		giftee_profile_published = GifteeProfile.objects.filter(published=True)

		return render(request, "fulfill.html", {"giftee_profiles_unpublished": giftee_profiles_unpublished,
		                                        "page": "fulfill", "giftee_profile_published": giftee_profile_published})