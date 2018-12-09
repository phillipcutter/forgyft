from django.utils.crypto import get_random_string


def get_slug(obj, length=6, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", underscoreSlug=False):
	while True:
		slug = get_random_string(length=length, allowed_chars=allowed_chars)

		if underscoreSlug:
			objs_with_slug = type(obj).objects.filter(_slug=slug)
		else:
			objs_with_slug = type(obj).objects.filter(slug=slug)
		if len(objs_with_slug) <= 0:
			return slug


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip