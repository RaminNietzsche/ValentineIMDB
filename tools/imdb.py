import requests
import simplejson

def get_data(data):
	url = 'http://www.omdbapi.com/?t=%s&y=%s' %(data['name'], data['year'])
	response = requests.get(url);
	res = response.json()
	res['name'] = data['name']
	# print data['Plot']
	return data