import django
from django.db import models

# Create your models here.

class Interest(models.Model):
	interest = models.TextField()

	def add_product(self, **kwargs):
		try:
			return ScrapeProduct.objects.create(**kwargs, interest=self)
		except django.db.utils.DataError:
			return False

	def __str__(self):
		return "Interest: " + str(self.interest)

class ScrapeProduct(models.Model):

	interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
	title = models.TextField(null=True)
	description = models.TextField(null=True)
	price = models.FloatField(null=True)
	url = models.URLField()
	image_url = models.URLField(null=True)
