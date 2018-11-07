from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from forgyftapp.forms import GifteeProfileForm
from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.models import GifteeProfile


def index(request):
	if request.method == "POST":
		form = GifteeProfileForm(request.POST)
		if form.is_valid():
			form.save(user=request.user)
			return redirect("forgyftapp:index")
	else:
		form = GifteeProfileForm()

	return render(request, "cover.html", {"form": form})

@staff_member_required
def fulfill(request, profile=None):

	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if request.method == "POST":
			form = GiftIdeaForm(request.POST)
			if form.is_valid():
				form.save(user=request.user)
				return redirect("forgyftapp:index")
		else:
			form = GiftIdeaForm()


		return render(request, "fulfill.html", {"giftee_profile": giftee_profile, "form": form})
	else:
		giftee_profiles = GifteeProfile.objects.filter(fulfilled=False)

		return render(request, "fulfill.html", {"giftee_profiles": giftee_profiles})