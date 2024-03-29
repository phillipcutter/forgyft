from django.contrib import admin

# Register your models here.
from forgyftapp.models import User, GifteeProfile, GiftIdea, GiftFeedback, ScraperInterests, SampleGiftIdea, SampleGiftRequest

admin.site.register(User)
admin.site.register(GifteeProfile)
admin.site.register(GiftIdea)
admin.site.register(GiftFeedback)
admin.site.register(ScraperInterests)

admin.site.register(SampleGiftIdea)
admin.site.register(SampleGiftRequest)