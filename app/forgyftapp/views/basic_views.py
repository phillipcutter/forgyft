import bugsnag as bugsnag
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from forgyft import settings
from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet, GiftFeedbackForm, ScraperInterestsForm
from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.models import GifteeProfile, GiftIdea
from scraper.tasks import add


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

@login_required(login_url=settings.SIGNUP_URL)
def link_request(request, slug=None):
	if not slug:
		return redirect("forgyftapp:request")

	giftee_profile = GifteeProfile.fromSlug(slug)
	user = request.user

	if giftee_profile.has_user:
		return redirect("forgyftapp:request", slug=slug)

	giftee_profile.link_user(user)
	return redirect("forgyftapp:request", slug=slug)

def request(request, profile=None, slug=None):
	if slug:
		giftee_profile = GifteeProfile.fromSlug(slug)

		if not giftee_profile.published and not giftee_profile.has_user:
			return redirect("forgyftapp:index")
		elif not giftee_profile.published or (giftee_profile.has_user and not giftee_profile.user == request.user):
			return redirect("forgyftapp:request")

		if request.method == "POST":
			feedback_form = GiftFeedbackForm(request.POST, instance=giftee_profile.feedback)
			if feedback_form.is_valid():
				feedback = feedback_form.save(giftee_profile=giftee_profile)
				giftee_profile.feedback = feedback
				giftee_profile.save()
				return redirect("forgyftapp:request", slug=giftee_profile.slug)
		else:
			feedback_form = GiftFeedbackForm(instance=giftee_profile.feedback)

		hasFeedback = giftee_profile.feedback is not None

		return render(request, "request.html", {"giftee_profile": giftee_profile,
		                                        "ideas": GiftIdea.objects.filter(giftee_profile=giftee_profile),
		                                        "page": "request", "feedback_form": feedback_form,
		                                        "hasFeedback": hasFeedback})

	if not request.user.is_authenticated:
		return login_required()(request)(request)

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
				return redirect("forgyftapp:request", slug=giftee_profile.slug)
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
			return redirect("forgyftapp:request", slug=giftee_profile.slug)

		gift_idea.click()

		return redirect(gift_idea.link)
	else:
		return redirect("forgyftapp:request")


def gift_form_submitted(request):
	return render(request, "gift_form_submitted.html", {"page": "quiz"})

def gift_form(request):
	has_account = request.user.is_authenticated

	if request.method == "POST":
		form = GifteeProfileForm(request.POST, account=has_account)
		if form.is_valid():
			form.save(user=request.user, request=request)
			return redirect("forgyftapp:gift_form_submitted")
	else:
		form = GifteeProfileForm(account=has_account)

	return render(request, "gift_form.html", {"form": form, "page": "quiz"})




@staff_member_required
def fulfill(request, profile=None):
	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if request.method == "POST":
			gift_ideas = GiftIdeaFormSet(request.POST, instance=giftee_profile, prefix="gift_ideas")
			scrape_form = ScraperInterestsForm(request.POST, instance=giftee_profile.feedback, prefix="scrape_form")

			if 'gift_ideas' in request.POST:
				if gift_ideas.is_valid():
					gift_ideas.save()

					published = (request.POST.get("published", 'false') == 'true')

					if published:
						giftee_profile.submit(request)
					else:
						giftee_profile.unsubmit()

					return redirect("forgyftapp:fulfill", profile=profile)
			elif 'scrape_form' in request.POST:
				if scrape_form.is_valid():
					scraper_interests = scrape_form.save(giftee_profile=giftee_profile)
					giftee_profile.scraper_interests = scraper_interests
					giftee_profile.save()
					return redirect("forgyftapp:fulfill", profile=giftee_profile.pk)
		else:
			gift_ideas = GiftIdeaFormSet(instance=giftee_profile, prefix="gift_ideas")
			scrape_form = ScraperInterestsForm(instance=giftee_profile.feedback, prefix="scrape_form")

		scraper_status = ""
		scraper_results = None

		if giftee_profile.scraper_interests:
			scraper_status = "DONE" if giftee_profile.scraper_interests.generated else "WAIT"
			if giftee_profile.scraper_interests.generated:
				scraper_results = giftee_profile.scraper_interests.interest_objects.all()
		else:
			scraper_status = "FORM"

		published = giftee_profile.published

		return render(request, "fulfill.html", {
			"giftee_profile": giftee_profile,
			"gift_ideas": gift_ideas,
		    "page": "fulfill",
			"published": published,
			"scrape_form": scrape_form,
			"scraper_status": scraper_status,
			"scraper_results": scraper_results,
		})
	else:
		giftee_profiles_unpublished = GifteeProfile.objects.filter(published=False).order_by('created')
		giftee_profile_published = GifteeProfile.objects.filter(published=True).order_by('created')

		return render(request, "fulfill.html", {"giftee_profiles_unpublished": giftee_profiles_unpublished,
		                                        "page": "fulfill", "giftee_profile_published": giftee_profile_published})