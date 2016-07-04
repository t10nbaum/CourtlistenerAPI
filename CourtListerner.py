from Sensative import courtlistener_api_key
import requests
import pprint
import math

headers = {'Authorization': "Token " + courtlistener_api_key}


url = "https://www.courtlistener.com/api/rest/v3/clusters/?order_by=-date_filed&format=json"

response = requests.get( url, headers=headers)
results = response.json()["results"]
page = 1

def create_opinion_cluster_url(page):
	"""Dynamically creates the url for the opinion cluster pages. Includes filters and formatting and returns the url to request"""
	base_url = "https://www.courtlistener.com/api/rest/v3/clusters/?"
	format = "format=json"
	sort = "&order_by=-date_filed"
	page = "&page=" + str(page)
	url = base_url + format+ sort+ page
	return url

def create_response(url):
	"""Based on the URL from create_opinion_cluster_url, returns JSON of opinion cluster request"""
	return requests.get(url, headers=headers).json()
	


def num_of_pages(response):
	"""Return the number of pages. Each page has 20 results. Number of pages equals count of records divided by 20"""
	return math.ceil(int(response['count'])/20.0)

def get_court(case):
	"""Returns the court for each case listed in opinion cluster response"""
	url = case['docket']
	court_url = requests.get(url, headers=headers)
	court_url = court_url.json()['court']
	court_name = requests.get(court_url,headers=headers)
	court_name = court_name.json()['full_name']
	return court_name

"""Create a search term to use to search case names. If search term is given, cases are returned in reverse chronological order. If the search term is present, only matching cases are returned."""
search_term = str(raw_input("Enter your search term here:")).lower()
for page in range(1, int(num_of_pages(create_response(create_opinion_cluster_url(page))))):
	# print "Page %s url is: %s" % (page, create_opinion_cluster_url(page))
	
	for i in create_response(create_opinion_cluster_url(page))["results"]:
		
		if search_term:
			if search_term in i["case_name"].lower():
				
				print "(%s) %s was decided in the %s" % (page, i["case_name"], get_court(i))
		else:
			print "%s was decided in the %s" % (i["case_name"], get_court(i))
	
		