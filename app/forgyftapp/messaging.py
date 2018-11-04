import json

import requests

webhook_url = "***REMOVED***"

def broadcast_to_slack(message):
	return requests.post(webhook_url, json.dumps({"text": message}), json=True)