from django.shortcuts import render, redirect

# Create your views here.
from forgyftapp.forms import GifteeProfileForm


def index(request):
	if request.method == "POST":
		form = GifteeProfileForm(request.POST)

		if form.is_valid():
			form.save(user=request.user)
			return redirect("forgyftapp:index")
	else:
		form = GifteeProfileForm()

	return render(request, "index.html", {"form": form})