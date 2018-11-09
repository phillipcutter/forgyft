from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.
from django.db.models import Model
from django.dispatch import receiver
from django.http import Http404

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

class GifteeProfile(models.Model, OnCreate):
	interests = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fulfilled = models.BooleanField(default=False)


	def __str__(self):
		return f"Giftee Profile {self.pk}: {self.interests}"

	def onCreate(self):
		super().onCreate()
		broadcast_to_slack(f"Hey <!channel>, there was a new gift request created by {str(self.user)}. Login to the website to give gift suggestions.")


class GiftIdea(models.Model):
	idea = models.TextField()
	link = models.URLField()
	giftee_profile = models.ForeignKey(GifteeProfile, related_name="ideas", on_delete=models.PROTECT)


@receiver(models.signals.post_save)
def execute_after_save(sender, instance, created, *args, **kwargs):
	if issubclass(instance.__class__, OnCreate) and created:
		instance.onCreate()