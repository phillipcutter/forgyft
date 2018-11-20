import json

import requests

from forgyft import settings


def broadcast_to_slack(message):
	webhook_url = "***REMOVED***"
	return requests.post(webhook_url, json.dumps({"text": message}), json=True)

def debug_log(message):
	if settings.DEBUG:
		print(message)
		return
	webhook_url = "***REMOVED***"
	return requests.post(webhook_url, json.dumps({"text": message}), json=True)