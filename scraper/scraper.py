import functools

import dill as dill
import requests
from tqdm import tqdm
from google import google
from requests_futures.sessions import FuturesSession

output_file = "output2.txt"

def load():
	with open(output_file, "rb") as dill_file:
		interests = dill.load(dill_file)
	print(interests)
	return interests

class Interest:
	def __init__(self, interest, plural):
		self.interest = interest
		self.plural = plural
		self.links = []
		self.products = []



def get_links(url, session):
	r = session.get(api_url, params={"token": api_token, "url": url, "fields": "links"}).result()
	try:
		if not r.json().get("errorCode", None):
			links = r.json().get("objects", [None])[0].get("links")
			return filter_links(links)
		else:
			return []
	except:
		print("Error occured retrieving JSON from Diffbot call, HTTP code: " + str(r.status_code))
		return []


def filter_links(links):
	return [link for link in links if "/dp/" in link]

api_url = "https://api.diffbot.com/v3/article"
api_token = "2380b8630674273660e2d3654b3ec3cf"


def hook_factory(*factory_args, **factory_kwargs):
	def process_links(r, *args, **kwargs):
		interest = factory_kwargs.get("interest")
		# print("Callback")
		links = []
		try:
			if not r.json().get("errorCode", None):
				links = r.json().get("objects", [None])[0].get("links")
				links = filter_links(links)
		except:
			pass
		print("Callback for interest: " + interest.interest)
		interest.products.extend(links)

	return process_links

interests = [
	# Interest("skiing", "skiers"),
	# Interest("art", "artists"),
	# Interest("programming", "programmers"),
	# Interest("writing", "writers"),
	# Interest("gaming", "gamers"),
	# Interest("music", "music lovers")
	Interest("astrology", "astrology lovers"),
	Interest("physics", "physics lovers"),
	Interest("makeup", "makeup lovers"),
]


def main():
	session = FuturesSession(max_workers=64)

	for interest in interests:
		pages = 1
		results = google.search("Gifts for " + interest.plural, pages)
		for result in results:
			interest.links.append(result.link)

	async_requests = []

	print("Starting async calls")
	for interest in interests:
		for url in interest.links:
			async_requests.append(session.get(api_url, params={"token": api_token, "url": url, "fields": "links"},
			                     hooks={"response": hook_factory(interest=interest)}))


	for req in async_requests:
		print(req.result())

	print("All Requests Done")
	print("Pickle: " + str(dill.dumps(interests)))

	with open(output_file, "wb") as dill_file:
		dill.dump(interests, dill_file)



if __name__ == "__main__":
	main()