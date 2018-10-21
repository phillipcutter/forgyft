from django.contrib import admin

# Register your models here.
from forgyftapp.models import User, GifteeProfile

admin.site.register(User)
admin.site.register(GifteeProfile)