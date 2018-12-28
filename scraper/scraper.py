import dill as dill
import requests
from tqdm import tqdm
from google import google
import pickle

def load():
	with open("output.txt", "rb") as dill_file:
		interests = dill.load(dill_file)
	print(interests)

class Interest:
	interest = ""
	plural = ""
	links = []
	products = []

	def __init__(self, interest, plural):
		self.interest = interest
		self.plural = plural


def get_links(url):
	r = requests.get(api_url, params={"token": api_token, "url": url, "fields": "links"})
	if not r.json().get("errorCode", None):
		links = r.json().get("objects", [None])[0].get("links")
		return filter_links(links)
	else:
		return []


def filter_links(links):
	return [link for link in links if "/dp/" in link]

api_url = "https://api.diffbot.com/v3/article"
api_token = "20e3cd53421d6ade87c0b0569088b781"

interests = [
	Interest("skiing", "skiers"),
	Interest("art", "artists"),
	Interest("programming", "programmers"),
	Interest("writing", "writers"),
	Interest("gaming", "gamers"),
	Interest("music", "music lovers")
]

for interest in interests:
	pages = 2
	results = google.search("Gifts for " + interest.plural, pages)
	for result in results:
		interest.links = [result.link]

for interest in tqdm(interests):
	for url in tqdm(interest.links):
		links = get_links(url)
		interest.products.extend(links)

print("Done")
print("Pickle: " + str(dill.dumps(interests)))

with open("output.txt", "wb") as dill_file:
	dill.dump(interests, dill_file)