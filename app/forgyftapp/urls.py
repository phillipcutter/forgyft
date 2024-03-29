from django.conf.urls import url

from forgyftapp.views import basic_views, auth_views, expert_views

app_name = "forgyftapp"

urlpatterns = [
	url(r'^$', basic_views.index, name="index"),

	url(r'^experts/?$', expert_views.experts_index, name='experts_index'),
	url(r'^quiz/?$', basic_views.gift_form, name='gift_form'),
	url(r'^submit/?$', basic_views.gift_form_submitted, name='gift_form_submitted'),
	url(r'^submit/(?P<slug>[A-Za-z0-9]+)/?$', basic_views.gift_form_submitted, name='gift_form_submitted'),

	url(r'^request/?$', basic_views.request, name='request'),
	url(r'^request/(?P<profile>[0-9]+)/?$', basic_views.request, name='request'),
	url(r'^request/slug/(?P<slug>[A-Za-z0-9]+)/?$', basic_views.request, name='request'),
	url(r'^view_gift/(?P<gift>[0-9]+)/?$', basic_views.view_gift, name='view_gift'),

	url(r'^request/link/(?P<slug>[A-Za-z0-9]+)/?$', basic_views.link_request, name='link_request'),

	url(r'^fulfill/?$', basic_views.fulfill, name='fulfill'),
	url(r'^fulfill/(?P<profile>[0-9]+)/?$', basic_views.fulfill, name='fulfill'),
	url(r'^fulfill/(?P<profile>[0-9]+)/?$', basic_views.fulfill, name='fulfill'),

	url(r'^experts_profile/fulfill/(?P<slug>[A-Za-z0-9]+)/?$', expert_views.expert_fulfill, name='expert_fulfill'),

	# Static pages
	url(r'^terms/?$', basic_views.terms, name='terms'),
	url(r'^privacy/?$', basic_views.privacy, name='privacy'),
	url(r'^about/?$', basic_views.about, name='about'),
	url(r'^contact/?$', basic_views.contact, name='contact'),

	# Auth views
	url(r'^signup/?$', auth_views.signup, name='signup'),
	url(r'^login/?$', auth_views.login_view, name='login'),
	url(r'^logout/?$', auth_views.logout_view, name='logout'),

	## Expert Auth
	url(r'^experts_signup/?$', expert_views.signup, name='experts_signup'),
	url(r'^expert_profile/?$', expert_views.profile, name='expert_profile'),


	url(r'^account_activation_send/?$', auth_views.account_activation_sent, name="account_activation_sent"),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    auth_views.activate, name='activate'),

	url(r'^reset/?$', auth_views.reset_password, name="reset"),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    auth_views.reset_confirm, name='password_reset_confirm'),
	url(r'^reset/success/$', auth_views.reset_success, name='reset_success'),
	url(r'^reset/finished/$', auth_views.reset_finished, name='reset_finished'),

]
