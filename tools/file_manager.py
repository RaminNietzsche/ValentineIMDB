#!/usr/bin/python

import os, fnmatch
import datetime

from text import simple_normalize
from imdb import get_data
import config

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

res = []
for types in config.movie_formats:
	f = find('*.'+types, '/file/Backup/Download/film/30/')
	for item in f:
		data = {}
		data['address'] = item
		file_name = simple_normalize(item.split('/')[-1])
		try:
			now = datetime.datetime.now()
			if int(file_name.split()[-1]) > 1800 and int(file_name.split()[-1]) < now.year:
				data['year'] = file_name.split()[-1]
				data['name'] = file_name.replace(data['year'], '')
		except:
			data['year'] = ''
			data['name'] = file_name
		if data['name'] != 'sample':
			dup = False
			# for rec in res:
			# 	if rec['name'] == data['Title']:
			# 		dup = True
			# 		break
			# if not dup:
			res.append(get_data(data))

for item in res:
	print 'Name: %s' %(item['name'])
	try:
		print 'Title: %s' %(item['Title'])
	except :
		pass
	try:
		print 'Year: %s' %(item['Year'])
	except :
		pass		
	try:
		print 'Rate: %s' %(item['imdbRating'])
	except :
		pass		
	print '----------'
