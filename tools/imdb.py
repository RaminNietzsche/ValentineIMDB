import requests
import simplejson

def get_data(data):
	url = 'http://www.omdbapi.com/?t=%s&y=%s' %(data['name'], data['year'])
	response = requests.get(url);
	res = response.json()
	if res['Response'] == 'False':
		res = search_move(data['name'])
	res['name'] = data['name']
	return res

def search_move(name):
	url = 'http://www.omdbapi.com/?s=%s' %(name)
	response = requests.get(url);
	res = response.json()
	if res['Response'] == 'False':
		res['Title'] = "404! -----> kolan Not Found ;)"
	else:
		url = 'http://www.omdbapi.com/?i=%s' %(res['Search'][0]['imdbID'])
		response = requests.get(url);
		res = response.json()
	return res