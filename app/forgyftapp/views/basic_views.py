from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from forgyftapp.forms import GifteeProfileForm, GiftIdeaForm, GiftIdeaFormSet
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

	return render(request, "homepage.html", {"form": form})


class GifteeList(ListView):
	model = GifteeProfile


class GiftIdeaCreate(CreateView):
	model = GifteeProfile
	fields = ['interests']
	success_url = reverse_lazy('forgyftapp:giftee-list')

	def get_context_data(self, **kwargs):
		data = super(GiftIdeaCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['giftideas'] = GiftIdeaFormSet(self.request.POST)
		else:
			data['giftideas'] = GiftIdeaFormSet()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		giftideas = context['giftideas']
		with transaction.atomic():
			self.object = form.save()

			if giftideas.is_valid():
				giftideas.instance = self.object
				giftideas.save()
		return super(GiftIdeaCreate, self).form_valid(form)

@staff_member_required
def fulfill(request, profile=None):

	if profile:
		giftee_profile = get_object_or_404(GifteeProfile, pk=profile)

		if request.method == "POST":
			form = GiftIdeaForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect("forgyftapp:index")
		else:
			form = GiftIdeaForm()


		return render(request, "fulfill.html", {"giftee_profile": giftee_profile, "form": form})
	else:
		giftee_profiles = GifteeProfile.objects.filter(fulfilled=False)

		return render(request, "fulfill.html", {"giftee_profiles": giftee_profiles})