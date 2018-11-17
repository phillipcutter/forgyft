from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.db.models import Model
from django.dispatch import receiver
from django.http import Http404
from django.urls import reverse

from forgyftapp.messaging import broadcast_to_slack
from forgyftapp.py_utils import django_utils


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


class User(AbstractUser, Slug):
	email_confirmed = models.BooleanField(default=False)

	def onCreate(self):
		super().onCreate()
		self.paypal_email = self.email
		self.save()

class gender:
	MALE = "MALE"
	FEMALE = "FEMALE"
	OTHER = "OTHER"

	GENDERS = ["Male", "Female", "Other"]
	GENDER_CHOICES = ((MALE, "Male"),
	                  (FEMALE, "Female"),
	                  (OTHER, "Other"))

class GifteeProfile(models.Model, OnCreate):
	name = models.TextField(max_length=150)
	gender = models.CharField(max_length=80, choices=gender.GENDER_CHOICES)
	age = models.IntegerField()
	relationship = models.TextField(max_length=6000)
	price_upper = models.IntegerField()
	interests = models.TextField(max_length=6000)
	existing_related_items = models.TextField(max_length=6000)
	extra_info = models.TextField(max_length=6000)

	published = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	@property
	def status(self):
		if self.published:
			return "Your gift ideas are ready, click on the button below to view them."
		else:
			return "We're still deciding on the perfect gifts, please check back soon."

	def submit(self, request):
		view_url = request.build_absolute_uri(reverse("forgyftapp:request", kwargs={"profile": self.pk}))
		send_mail(f"Your gift ideas for {self.name} are ready",
		          f"To view your gift ideas click this link: {view_url}",
		          "noreply@forgyft.com",
		          [self.user.email],
		          html_message=f"To view your gift ideas click <a href=\"{view_url}\">here</a>")
		self.published = True
		self.save()

	def unsubmit(self):
		self.published = False
		self.save()

	def gender_string(self):
		choices = {}

		for choice in gender.GENDER_CHOICES:
			choices[choice[0]] = choice[1]

		return choices.get(self.gender)


	def __str__(self):
		return f"Giftee Profile {self.pk}: {self.interests}"

	def onCreate(self):
		super().onCreate()
		fulfillUrl = reverse("forgyftapp:fulfill", kwargs={"profile": self.pk})
		broadcast_to_slack(f"Hey <!channel>, there was a new gift request created by {str(self.user)}. "
		                   f"Enter gift ideas <{fulfillUrl}|here>")


class GiftIdea(models.Model):
	idea = models.TextField()
	link = models.URLField(max_length=600)
	published = models.BooleanField(default=False)
	giftee_profile = models.ForeignKey(GifteeProfile, related_name="ideas", on_delete=models.PROTECT)


@receiver(models.signals.post_save)
def execute_after_save(sender, instance, created, *args, **kwargs):
	if issubclass(instance.__class__, OnCreate) and created:
		instance.onCreate()