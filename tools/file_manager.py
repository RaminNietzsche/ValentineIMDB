#!/usr/bin/python

import os, fnmatch
import datetime

from text import simple_normalize
from imdb import get_data, Runner
import config

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

res = []
file_lst = []
f = find('*', '/file/Backup/Download/film/30/')
for item in f:
	if item.split('.')[-1] in config.movie_formats:
		file_lst.append(item)

for item in Runner(file_lst):
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