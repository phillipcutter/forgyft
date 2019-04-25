import bugsnag as bugsnag
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from forgyft import settings
from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet, GiftFeedbackForm, ScraperInterestsForm, \
	ExpertAssignForm
from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.models import GifteeProfile, GiftIdea, User
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
			giftee_profile = form.save(user=request.user, request=request)

			if has_account and request.user.demo_fulfill:
				GiftIdea.objects.create(
					idea="3D Origami Starter Kit",
					link="https://www.etsy.com/listing/654042850/3d-origami-triangle-starter-pack-with-7?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=origami&ref=sr_gallery-3-16&organic_search_click=1&sca=1",
					image="https://i.etsystatic.com/16367318/r/il/8c18d2/1720551816/il_794xN.1720551816_jjhe.jpg",
					explanation="This gift is PERFECT for your friend Sarah! This 3D origami kit factors in her love for Origami while elevating it to a new experience. This kit has over 1000 pieces in it so she'll be able to make hundreds of origami just from this box!",
					giftee_profile=giftee_profile
                ),
				GiftIdea.objects.create(
					idea="Scrapbook + Bowtie",
					link="https://www.amazon.com/gp/product/B075F5T61Z/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=forgift06-20&creative=9325&linkCode=as2&creativeASIN=B075F5T61Z&linkId=266a774d8f271fbf69301743b85392a7",
					image="https://images-na.ssl-images-amazon.com/images/I/71sGq4PojJL._SL1500_.jpg",
					explanation="This is SUPER creative because it’ll show Sarah that you care about her so much! He "
					            "can put hundreds of different pictures of them together, and it’ll make Sarah feel really special and loved.",
					giftee_profile=giftee_profile
				),
				GiftIdea.objects.create(
					idea="Personalized + Quirky Makeup Bag",
					link="https://www.etsy.com/listing/521080058/best-friend-gift-makeup-case?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=personalized+gifts&ref=sr_gallery-2-14&organic_search_click=1&frs=1",
					image="https://i.etsystatic.com/9389727/r/il/f33fda/1296251237/il_794xN.1296251237_f3la.jpg",
					explanation="This gift is the BEST for Sarah! It's perfect for her interest in makeup because she'll be able to store all her makeup in that bag! And we'll personalize the gift just for Sarah!",
					giftee_profile=giftee_profile
				)
				giftee_profile.submit(request)

			return redirect("forgyftapp:gift_form_submitted")
	else:
		if has_account and request.user.demo_fulfill:
			form = GifteeProfileForm({
				"name": "Sarah",
				"gender": "FEMALE",
				"age": 15,
				"relationship": "Close Friend",
				"occasion": "Birthday",
				"price_upper": 50,
				"interests": "Makeup, Flowers, Origami",
				"personality_traits": "Creative, Outgoing, Sweet"

			}, account=has_account)
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
			expert_assign = ExpertAssignForm(request.POST, prefix="expert_assign")

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
			elif 'expert_assign' in request.POST:
				if expert_assign.is_valid():
					expert_user = expert_assign.clean()["expert"]

					if expert_user != giftee_profile.expert:
						gift_request_link = request.build_absolute_uri(reverse("forgyftapp:expert_fulfill",
						                                                       kwargs={"slug": giftee_profile.slug}))
						send_mail(
							"You Have A New Gift Request",
f"""
Hey,

You have a new gift request to fill out. Just sign in on www.forgift.org and head to the fulfill tab or just head over to {gift_request_link} to fulfill your new gift request. Please try to fill it out within the next 24 hours with at least three gift ideas.      

Thanks for participating in the Forgift Expert Program!

The Forgift Team
""",
							"Forgift <support@forgift.org>",
							[expert_user.email],
							html_message=
f"""
<p>
Hey,<br><br>

You have a new gift request to fill out. Just sign in on www.forgift.org and head to the fulfill tab or just head over to {gift_request_link} to fulfill your new gift request. Please try to fill it out within the next 24 hours with at least three gift ideas.<br><br>    

Thanks for participating in the Forgift Expert Program!<br><br>

The Forgift Team<br>
</p>
"""
						)

						giftee_profile.expert = expert_user
						giftee_profile.save()
					return redirect("forgyftapp:fulfill", profile=giftee_profile.pk)
		else:
			gift_ideas = GiftIdeaFormSet(instance=giftee_profile, prefix="gift_ideas")
			scrape_form = ScraperInterestsForm(instance=giftee_profile.feedback, prefix="scrape_form")
			expert_assign = ExpertAssignForm(prefix="expert_assign", initial={'expert': giftee_profile.expert})


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
			"expert_assign": expert_assign
		})
	else:
		giftee_profiles_unpublished = GifteeProfile.objects.filter(published=False).order_by('created')
		giftee_profile_published = GifteeProfile.objects.filter(published=True).order_by('created')

		return render(request, "fulfill.html", {"giftee_profiles_unpublished": giftee_profiles_unpublished,
		                                        "page": "fulfill", "giftee_profile_published": giftee_profile_published})