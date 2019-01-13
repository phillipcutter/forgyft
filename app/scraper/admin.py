from django.contrib import admin

# Register your models here.
from scraper.models import Interest, ScrapeProduct

admin.site.register(Interest)
admin.site.register(ScrapeProduct)