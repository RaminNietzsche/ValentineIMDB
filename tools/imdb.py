import requests
import simplejson
import time
import threading
from text import simple_normalize
import datetime
from DBbuilder import process_img

def Runner(files):
	threads = []
	for item in files:
		tr = threading.Thread(target=get_data, args = (item,))
		tr.start()
		threads.append(tr)
	for i in threads:
		i.join()
	return movie_lst

def get_data(file):
	data = {}
	data['address'] = file
	file_name = simple_normalize(file.split('/')[-1])
	now = datetime.datetime.now()
	data['year'] = ''
	data['name'] = file_name
	
	try:
		if int(file_name.split()[-1]) > 1800 and int(file_name.split()[-1]) < now.year:
			data['year'] = file_name.split()[-1]
			data['name'] = file_name.replace(data['year'], '')
	except:
		data['year'] = ''
		data['name'] = file_name
	if data['name'] == 'sample':
		return

	url = 'http://www.omdbapi.com/?t=%s&y=%s' %(data['name'], data['year'])
	response = requests.get(url);
	res = response.json()
	if res['Response'] == 'False':
		res = search_move(data['name'])
	res['name'] = data['name'] 
	to_db(res)

def search_move(name):
	url = 'http://www.omdbapi.com/?s=%s' %(name)
	response = requests.get(url);
	res = response.json()
	try:
		url = 'http://www.omdbapi.com/?i=%s' %(res['Search'][0]['imdbID'])
		response = requests.get(url);
		res = response.json()
	except:
		res['Title'] = "404! -----> kolan Not Found ;)"
	res['name'] = name
	return (res)

movie_lst = []
def to_db(item):
	movie_lst.append(item)