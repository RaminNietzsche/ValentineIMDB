#!/usr/bin/python

import os, fnmatch
import datetime
import sqlite3

from text import simple_normalize
from imdb import get_data, Runner
from DBbuilder import create_database, is_in_db, add_to_db
import config

def find(pattern, path):
	result = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(os.path.join(root, name))
	return result

def check_and_setup():
    # check needed folder and creat them if they are'nt exist!
    try: os.mkdir(config.mdb_dir)
    except OSError, e: pass

    try: os.mkdir(config.images_folder)
    except OSError, e: pass

    if (os.path.exists(config.db_file) and \
            config.config['db_version'] < config.db_version):
        # db_version is old, make new db file
        os.unlink(config.db_file)

    if (not os.path.exists(config.db_file)):
        create_db = True
    else:
        create_db = False

    conn = sqlite3.connect(config.db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if (create_db):
        create_database(conn, cur)

        config.config['db_version'] = config.db_version
        config.config.write()

    return conn, cur


def main():
	conn, cur = check_and_setup()
	res = []
	file_lst = []
	now = datetime.datetime.now()
	
	f = find('*', '/file/Backup/Download/film/')

	for item in f:
		if item.split('.')[-1] in config.movie_formats:
			file_name = simple_normalize(item.split('/')[-1])
			try:
				if int(file_name.split()[-1]) > 1800 and int(file_name.split()[-1]) < now.year:
					year = file_name.split()[-1]
					file_name = file_name.replace(year, '')
			except:
				pass
			if is_in_db(conn, cur, file_name, 'movies') or file_name == 'sample':
				pass
			else:
				file_lst.append(item)

	for item in Runner(file_lst):
		print item['name']
		add_to_db(item['name'], item, conn, cur)


if __name__ == '__main__':
    main()