import bugsnag as bugsnag
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet, GiftFeedbackForm
from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.models import GifteeProfile, GiftIdea


def index(request):
	return render(request, "homepage.html", {"page": "home"})

def terms(request):
	return render(request, "static/terms.html")

def about(request):
	return render(request, "static/about.html", {"page": "about"})

def contact(request):
	return render(request, "static/contact.html")

def privacy(request):
	return render(request, "static/privacy.html")

@login_required
def request(request, profile=None):
	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if not giftee_profile.published or not giftee_profile.user == request.user:
			return redirect("forgyftapp:request")

		if request.method == "POST":
			feedback_form = GiftFeedbackForm(request.POST, instance=giftee_profile.feedback)
			if feedback_form.is_valid():
				feedback = feedback_form.save(giftee_profile=giftee_profile)
				giftee_profile.feedback = feedback
				giftee_profile.save()
				return redirect("forgyftapp:request", profile=profile)
		else:
			feedback_form = GiftFeedbackForm(instance=giftee_profile.feedback)

		hasFeedback = giftee_profile.feedback is not None

		return render(request, "request.html", {"giftee_profile": giftee_profile,
		                                        "ideas": GiftIdea.objects.filter(giftee_profile=giftee_profile),
		                                        "page": "request", "feedback_form": feedback_form,
		                                        "hasFeedback": hasFeedback})
	else:
		giftee_profiles = GifteeProfile.objects.filter(user=request.user)

		return render(request, "request.html", {"giftee_profiles": giftee_profiles, "page": "request"})


@login_required
def view_gift(request, gift=None):
	if gift:
		gift_idea = get_object_or_404(GiftIdea, pk=gift)
		giftee_profile = gift_idea.giftee_profile

		if not giftee_profile.published or not giftee_profile.user == request.user:
			return redirect("forgyftapp:request", profile=giftee_profile.pk)

		gift_idea.click()

		return redirect(gift_idea.link)
	else:
		return redirect("forgyftapp:request")


def gift_form_submitted(request):
	return render(request, "gift_form_submitted.html", {"page": "request"})

def gift_form(request):
	if request.method == "POST":
		form = GifteeProfileForm(request.POST)
		if form.is_valid():
			form.save(user=request.user, request=request)
			return redirect("forgyftapp:gift_form_submitted")
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

				return redirect("forgyftapp:fulfill", profile=profile)
		else:
			gift_ideas = GiftIdeaFormSet(instance=giftee_profile)

		published = giftee_profile.published or (hasattr(gift_ideas.forms[0], "cleaned_data") and gift_ideas.forms[0].cleaned_data["published"])

		return render(request, "fulfill.html", {"giftee_profile": giftee_profile, "gift_ideas": gift_ideas,
		                                        "page": "fulfill", "published": published})
	else:
		giftee_profiles_unpublished = GifteeProfile.objects.filter(published=False).order_by('-created')
		giftee_profile_published = GifteeProfile.objects.filter(published=True).order_by('-created')

		return render(request, "fulfill.html", {"giftee_profiles_unpublished": giftee_profiles_unpublished,
		                                        "page": "fulfill", "giftee_profile_published": giftee_profile_published})