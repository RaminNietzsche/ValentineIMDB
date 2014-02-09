#!/usr/bin/python

import sqlite3
import re
import config
import os, sys

if config.defaults['proxy'] != 'None':
    set_proxy = True
    try:
        import requesocks as requests
    except Exception, e:
        set_proxy = False
        import requests
else:
    set_proxy = False
    import requests

def create_database(conn, cur):
    cur.execute('''CREATE TABLE movies (
            filename TEXT,
            title TEXT,
            year INTEGER,
            released TEXT,
            rating REAL,
            runtime TEXT,
            director TEXT,
            plot TEXT,
            poster TEXT,
            imdbID TEXT
            )''')
    cur.execute('''CREATE TABLE actors (
            name TEXT,
            imdbID TEXT
            )''')
    cur.execute('''CREATE TABLE genre (
            genre TEXT,
            imdbID TEXT
            )''')    
    cur.execute('CREATE UNIQUE INDEX filename_index ON movies (filename)')
    cur.execute('CREATE UNIQUE INDEX name_index ON actors (name, imdbID)')
    cur.execute('CREATE UNIQUE INDEX genre_index ON genre (genre, imdbID)')

    conn.commit()


def add_to_db(filename, file_data, conn, cur):
    if 'Year' not in file_data.keys():
        file_data['Year'] = "----"
    if 'Released' not in file_data.keys():
        file_data['Released'] = "----"
    if 'imdbRating' not in file_data.keys():
        file_data['imdbRating'] = "----"
    if 'Runtime' not in file_data.keys():
        file_data['Runtime'] = "----"
    if 'Director' not in file_data.keys():
        file_data['Director'] = "----"
    if 'Plot' not in file_data.keys():
        file_data['Plot'] = "----"
    if 'Poster' not in file_data.keys():
        file_data['Poster'] = "N/A"
    if 'imdbID' not in file_data.keys():
        file_data['imdbID'] = "----"
    
    if file_data['Title'] == "404! -----> kolan Not Found ;)":
        return

    args_mv = [filename, file_data['Title'], file_data['Year'],
        file_data['Released'], file_data['imdbRating'],
        file_data['Runtime'], file_data['Director'],
        file_data['Plot'], file_data['Poster'], file_data['imdbID']]

    if (is_in_db(conn, cur, filename, 'movies')):
        return

    for item in file_data['Actors'].split(','):
        args_actr = [item, file_data['imdbID']]
        cur.execute('INSERT INTO actors VALUES(?,?)',
                tuple(args_actr))

    for item in file_data['Genre'].split(','):
        args_gnr = [item, file_data['imdbID']]
        cur.execute('INSERT INTO genre VALUES(?,?)',
                tuple(args_gnr))

    cur.execute('INSERT INTO movies VALUES(?,?,?,?,?,?,?,?,?,?)',
            tuple(args_mv))

    if 'Poster' in file_data.keys():
        process_img(file_data['Poster'], file_data['name'])

    conn.commit()

def process_img(poster, filename):
    if (poster is None or poster == 'N/A'):
        return
    img_url = poster[:-7] + config.img_size + '.jpg'
    img_file = os.path.join(config.images_folder, filename + '.jpg')
    img_fh = open(img_file, 'wb')
    try:
        if set_proxy :
            img_fh.write(requests.get(img_url ,proxies=config.proxyDict).content)
        else:
            img_fh.write(requests.get(img_url).content)
    except requests.RequestException, e:
        # do nothing?
        pass
    img_fh.close()


def is_in_db(conn, cur, key_val, db):
    if conn is None:
        return False
    else:
        if db == 'movies':
            key = 'filename'
        elif db  == 'actors':
            key = 'name'
        elif db == 'genre':
            key = 'genre'

        res = cur.execute('SELECT * FROM '+ db +' WHERE '+ key +'=?',
                          (key_val,)).fetchall()
        if len(res) > 0:
            return True
        else:
            return False


def get_from_db(conn, cur, filename):
    res = cur.execute('SELECT * FROM movies WHERE filename=?',
            (filename,)).fetchall()
    return res[0]