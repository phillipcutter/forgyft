from django.conf.urls import url

from forgyftapp.views import basic_views, auth_views

app_name = "forgyftapp"

urlpatterns = [
	url(r'^$', basic_views.index, name="index"),
	url(r'^fulfill/?$', basic_views.fulfill, name='fulfill'),
	url(r'^fulfill/(?P<profile>[0-9]+)/?$', basic_views.fulfill, name='fulfill'),

	# Auth views
	url(r'^signup/?$', auth_views.signup, name='signup'),
	url(r'^login/?$', auth_views.login_view, name='login'),
	url(r'^logout/?$', auth_views.logout_view, name='logout'),

	url(r'^account_activation_send/?$', auth_views.account_activation_sent, name="account_activation_sent"),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    auth_views.activate, name='activate'),

	url(r'^reset/?$', auth_views.reset_password, name="reset"),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    auth_views.reset_confirm, name='password_reset_confirm'),
	url(r'^reset/success/$', auth_views.reset_success, name='reset_success'),
	url(r'^reset/finished/$', auth_views.reset_finished, name='reset_finished'),
	url(r'list/?$', basic_views.GifteeList.as_view(), name='giftee-list'),
	url(r'idea/add/?$', basic_views.GiftIdeaCreate.as_view(), name='giftee-add'),

]