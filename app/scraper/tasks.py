# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.apps import apps
from django.http import Http404

# from scraper.models import Interest
from forgyft import settings
from forgyftapp.util.amazon_utils import amazonify
from scraper.scraper import scrape


@shared_task
def scrape_for_giftee_profile(giftee_profile_slug):
	try:
		giftee_profile = apps.get_model('forgyftapp', 'GifteeProfile').fromSlug(giftee_profile_slug)
	except Http404 as e:
		print("Giftee profile given does not exist")
		raise e

	scraper_interests = giftee_profile.scraper_interests

	interests = scrape(scraper_interests.interests_arr)
	interest_objects = []

	for interest in interests:
		interest_object = apps.get_model('scraper', 'Interest').objects.create(interest=interest.plural)
		for product in interest.products:
			try:
				price = float(product.price)
			except:
				price = float(0)
			url = amazonify(product.url, settings.AMAZON_AFFILIATE_TAG)
			if not url:
				url = product.url
			interest_object.add_product(
				title=product.title,
				description=product.descripton,
				price=price,
				url=url,
				image_url=product.image_url
			)
			interest_object.save()
		interest_objects.append(interest_object)

	scraper_interests.done_generating(interest_objects)
	print("Finished scraping")

@shared_task
def add(x, y):
	print("TASK4: " + str(x + y))
	return x + y