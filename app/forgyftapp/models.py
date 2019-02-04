import random

import requests
import tldextract as tldextract
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models

# Create your models here.
from django.db.models import Model
from django.dispatch import receiver
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from forgyft import settings
from forgyftapp.messaging import broadcast_to_slack, debug_log
from forgyftapp.util import django_utils
from forgyftapp.util.django_utils import rand_slug
from scraper.tasks import scrape_for_giftee_profile


class gender:
	MALE = "MALE"
	FEMALE = "FEMALE"
	OTHER = "OTHER"

	GENDERS = ["Male", "Female", "Other"]
	GENDER_CHOICES = ((MALE, "Male"),
	                  (FEMALE, "Female"),
	                  (OTHER, "Other"))


class OnCreate:
	def onCreate(self):
		pass

class Slug(OnCreate, models.Model):
	_slug = models.SlugField(max_length=7, blank=True)

	def onCreate(self):
		super().onCreate()
		self._slug = self.slug
		self.save()

	@property
	def slug(self):
		if not self._slug:
			newSlug = django_utils.get_slug(self, length=7, underscoreSlug=True)
			self._slug = newSlug
			self.save()
		return self._slug

	@classmethod
	def fromSlug(cls, slug, case_insensitive=True):
		if case_insensitive:
			slug = slug.upper()
		obj = cls.objects.filter(_slug=slug)

		if obj.count() == 0:
			raise Http404(f"No {cls.__name__} found with the ID {str(slug)}")
		elif obj.count() > 1:
			raise MultipleObjectsReturned(f"Multiple {cls.__name__}s found with ID " + str(slug))
		else:
			listing = obj.first()

		return listing

	class Meta:
		abstract = True

class SampleGiftRequest(models.Model):
	_SAMPLE_OCCASIONS = ["Birthday", "Anniversary", "Valentine's Day", "Christmas", "Hanukkah"]

	gender = models.CharField(max_length=80, choices=gender.GENDER_CHOICES)
	age = models.IntegerField()
	occasion = models.TextField(max_length=6000)
	relationship = models.TextField(max_length=6000)
	price_upper = models.IntegerField()
	interests = models.TextField(max_length=6000)

	def gender_string(self):
		choices = {}

		for choice in gender.GENDER_CHOICES:
			choices[choice[0]] = choice[1]

		return choices.get(self.gender)

	@classmethod
	def fromExpert(cls, expert):
		if not expert.is_expert:
			return None

		sample = cls()
		sample.gender = expert.expert_gender
		sample.age = expert.expert_age + random.randint(-1, 1)
		sample.occasion = random.choice(cls._SAMPLE_OCCASIONS)
		sample.relationship = "Close Friend"
		sample.price_upper = round(random.randint(6, 90), -1)
		sample.interests = "Basketball, " + expert.expert_interests + ", drawing"
		sample.save()
		return sample


class SampleGiftIdea(models.Model, OnCreate):
	idea = models.TextField()
	link = models.URLField(max_length=2400)
	image = models.URLField(max_length=2400, blank=True, null=True)
	explanation = models.TextField()
	published = models.BooleanField(default=False)
	sample_giftee_profile = models.ForeignKey(SampleGiftRequest, related_name="ideas", on_delete=models.CASCADE)
	clicks = models.IntegerField(default=0)

	@property
	def domain(self):
		return tldextract.extract(self.link).domain


class User(AbstractUser, Slug):
	email_confirmed = models.BooleanField(default=False)

	is_expert = models.BooleanField(default=False)
	expert_age = models.IntegerField(null=True, blank=True)
	expert_gender = models.CharField(max_length=80, choices=gender.GENDER_CHOICES)
	expert_interests = models.TextField(null=True, blank=True)
	_expert_sample_gift_request = models.OneToOneField(SampleGiftRequest, on_delete = models.SET_NULL, null=True,
	                                                  blank=True)

	@property
	def expert_sample_gift_request(self):
		if self._expert_sample_gift_request:
			return self._expert_sample_gift_request
		else:
			self._expert_sample_gift_request = SampleGiftRequest.fromExpert(self)
			self.save()
			return self.expert_sample_gift_request

	def onCreate(self):
		super().onCreate()
		self.save()



class GiftFeedback(models.Model, OnCreate):

	rating = models.IntegerField()
	feedback = models.TextField(max_length=6000)
	bought = models.BooleanField()

	def onCreate(self):
		super().onCreate()
		fulfillUrl = settings.ABSOLUTE_URI + reverse("forgyftapp:fulfill", kwargs={"profile": self.giftee_profile.pk})
		debug_log(f"User submitted feedback for gift ideas. View it <{fulfillUrl}|here>.")
		broadcast_to_slack(f"Hey <!channel>, a user submitted feedback for gift ideas."
		                   f" View it <{fulfillUrl}|here>.")

class ScraperInterests(models.Model, OnCreate):
	interests = models.TextField(null=True, default=None, blank=True)

	interest_objects = models.ManyToManyField("scraper.Interest")

	@property
	def generated(self):
		# Oh Python and your one-liners
		return sum([len(interest.scrapeproduct_set.all()) for interest in self.interest_objects.all()]) > 0

	@property
	def interests_arr(self):
		return [interest.strip() for interest in self.interests.split(",")]

	def onCreate(self):
		super().onCreate()
		print("Kicking off scraper for scraper interests")
		scrape_for_giftee_profile.delay(self.giftee_profile.slug)

	def done_generating(self, interests):
		for interest in interests:
			self.interest_objects.add(interest)
		self.save()



class GifteeProfile(Slug):
	name = models.TextField(max_length=150)
	gender = models.CharField(max_length=80, choices=gender.GENDER_CHOICES)
	age = models.IntegerField()
	relationship = models.TextField(max_length=6000)
	price_upper = models.IntegerField()
	interests = models.TextField(max_length=6000)
	existing_related_items = models.TextField(max_length=6000)
	extra_info = models.TextField(max_length=6000, blank=True, null=True)
	occasion = models.TextField(max_length=6000)

	published = models.BooleanField(default=False)

	emailed_about_publish = models.BooleanField(default=False)

	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	email = models.EmailField(null=True)

	feedback = models.OneToOneField(GiftFeedback, on_delete=models.SET_NULL, null=True, blank=True)
	scraper_interests = models.OneToOneField(ScraperInterests, on_delete=models.SET_NULL, null=True, blank=True)

	created = models.DateTimeField(editable=False, null=True, blank=True)

	ip_address = models.GenericIPAddressField(null=True, default=None)

	_location = models.TextField(null=True, default=None, blank=True)


	def link_user(self, user):
		self.user = user
		self.save()

	@property
	def idea_clicks(self):
		clicks = 0
		for idea in self.ideas.all():
			clicks += idea.clicks
		return clicks

	@property
	def location(self):
		if self._location:
			return self._location
		else:
			#TODO: Make this asynchronous
			r = requests.get("http://api.ipstack.com/" + str(self.ip_address),
		                  params={"access_key": settings.IPSTACK_KEY})
			results = r.json()
			try:
				location_string = f"{results['city']}, {results['region_name']}, {results['country_name']}"
			except:
				location_string = "Unknown Location"
			self._location = location_string
			self.save()
			return location_string


	@property
	def email_address(self):
		if self.has_user:
			return self.user.email
		else:
			return self.email

	@property
	def has_user(self):
		return bool(self.user)

	@property
	def user_full_name(self):
		if self.user:
			return self.user.get_full_name()
		else:
			return self.email

	@property
	def status(self):
		if self.published:
			return "Your gift ideas are ready, click on the button below to view them."
		else:
			return "We're still deciding on the perfect gifts, please check back soon."

	def submit(self, request):
		if not self.emailed_about_publish:
			debug_log(f"Submitted gift ideas for {self.name}, as requested by {self.user_full_name}")
			if self.has_user:
				email = self.user.email
			else:
				email = self.email

			subject, from_email, to_email = \
				f"Your gift ideas for {self.name} are ready", \
				"Forgift <support@forgift.org>", \
				email

			view_url = request.build_absolute_uri(reverse("forgyftapp:request", kwargs={"slug": self.slug}))
			html_content = render_to_string("email/ideas_ready.html", {"view_url": view_url})
			text_content = strip_tags(html_content)

			msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			# send_mail(,
			#           f"To view your gift ideas click this link: {view_url}",
			#           ,
			#           [email],
			#           html_message=f"To view your gift ideas click <a href=\"{view_url}\">here</a>")
			self.emailed_about_publish = True
		self.published = True
		self.save()

	def unsubmit(self):
		if self.published:
			debug_log(f"Unsubmitted gift ideas for {self.name}, as requested by {self.user_full_name}")
			self.published = False
			self.save()

	def gender_string(self):
		choices = {}

		for choice in gender.GENDER_CHOICES:
			choices[choice[0]] = choice[1]

		return choices.get(self.gender)

	@property
	def admin_url(self):
		return reverse('admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))

	def __str__(self):
		return f"Giftee Profile {self.pk} for {self.name} from {self.user_full_name}"

	def onCreate(self):
		super().onCreate()
		self.created = timezone.now()
		self.save()
		if not settings.DEBUG:
			fulfillUrl = settings.ABSOLUTE_URI + reverse("forgyftapp:fulfill", kwargs={"profile": self.pk})
			debug_log(f"User with email address \"{self.email_address}\" submitted new gift request.")
			broadcast_to_slack(f"Hey <!channel>, there was a new gift request created by {self.user_full_name}. "
			                   f"Enter gift ideas <{fulfillUrl}|here>")


class GiftIdea(models.Model, OnCreate):
	idea = models.TextField()
	link = models.URLField(max_length=2400)
	image = models.URLField(max_length=2400, blank=True, null=True)
	explanation = models.TextField()
	published = models.BooleanField(default=False)
	giftee_profile = models.ForeignKey(GifteeProfile, related_name="ideas", on_delete=models.CASCADE)
	clicks = models.IntegerField(default=0)


	@property
	def domain(self):
		return tldextract.extract(self.link).domain


	def click(self):
		self.clicks += 1
		self.save()


@receiver(models.signals.post_save)
def execute_after_save(sender, instance, created, *args, **kwargs):
	if issubclass(instance.__class__, OnCreate) and created:
		instance.onCreate()