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

class Product:
	def __init__(self, title, description, price, url, image_url):
		self.title = title
		self.descripton = description
		self.price = price
		self.url = url
		self.image_url = image_url

class Interest:
	def __init__(self, plural):
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
product_api_url = "https://api.diffbot.com/v3/product"
api_token = "2380b8630674273660e2d3654b3ec3cf"


def hook_factory(*factory_args, **factory_kwargs):
	def process_links(r, *args, **kwargs):
		interest = factory_kwargs.get("interest")
		session = factory_kwargs.get("session")
		async_requests = factory_kwargs.get("async_requests")
		print("Callback for interest: " + interest.plural)
		# print("Callback")
		links = []
		try:
			if not r.json().get("errorCode", None):
				links = r.json().get("objects", [None])[0].get("links")
				links = filter_links(links)
		except:
			pass
		products = []

		for link in links:
			fields = "title,text,offerPrice,images.url"
			print("Queueing product api call")
			async_requests.append(session.get(product_api_url, params={"token": api_token, "url": link, "fields": "links"},
			                                  hooks={"response": hook_factory2(interest=interest, link=link)}))



	return process_links


def hook_factory2(*factory_args, **factory_kwargs):
	def process_product(r, *args, **kwargs):
		print("Product API callback")
		products = factory_kwargs.get("products")
		interest = factory_kwargs.get("interest")
		link = factory_kwargs.get("link")
		try:
			if not r.json().get("errorCode", None):
				product_json = r.json()
				objects = product_json.get("objects", [None])[0]
				title = objects.get("title")
				description = objects.get("text")
				price = objects.get("offerPrice").replace("$", "").replace(",", "")
				url = link
				image_url = objects.get("images")[0].get("url")
				interest.products.append(Product(title, description, price, url, image_url))
		except:
			pass

	return process_product

def scrape(interest_list):
	interests = []
	for interest in interest_list:
		# This class (Interest) which is basically just a struct, is completely unnecessary and should be removed
		interests.append(Interest(interest))

	session = FuturesSession(max_workers=128)

	print("Starting scrape Google search calls")
	for interest in interests:
		pages = 2
		results = google.search("Gifts for " + interest.plural, pages)
		for result in results:
			interest.links.append(result.link)

	async_requests = []

	print("Starting scrape async calls")
	for interest in interests:
		for url in interest.links:
			async_requests.append(session.get(api_url, params={"token": api_token, "url": url, "fields": "links"},
			                                  hooks={"response": hook_factory(interest=interest, session=session,
			                                                                  async_requests=async_requests)}))

	for req in async_requests:
		req.result()

	print("All Requests Done")

	return interests

def main():
	interests = scrape(["artists", "color lovers", "animal lovers"])

	print("All Requests Done")
	print("Pickle: " + str(dill.dumps(interests)))

	with open(output_file, "wb") as dill_file:
		dill.dump(interests, dill_file)



if __name__ == "__main__":
	main()