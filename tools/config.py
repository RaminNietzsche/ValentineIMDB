from configobj import ConfigObj
import os
import sys

movie_formats = ['avi', 'mkv', 'mp4', 'm4v', 'rmvb']

# Name Remove chars ;)
reject_words = ['dvd', 'xvid', 'brrip', 'r5', 'unrated', '720p', 'x264',
                    'klaxxon', 'axxo', 'br_300', '300mb', 'cd1', 'cd2', 
                    '1080p', 'BRrip', 'BluRay', 'GAZ', 'YIFY', 'BrRip',
                    'bitloks', 'AC3', 'JYK', 'R6', 'hdrip', 'etrg', 'deity',
                    'juggs', 'bdrip', 'readnfo', 'legi0n', 'sample','sam',]
brackets = ['(', ')', '[', ']', '{', '}']
bad_char = ['.', '-', '_']

defaults = {
        'update_last_checked': '0',
        'db_version': '0.1',
}

img_size = '300'

version = u'0.1'
db_version = u'0.1'

mdb_dir = os.path.join(os.path.expanduser('~'), u'.mdb')
db_file = os.path.join(mdb_dir, u'mdbdata.sqlite')
images_folder = os.path.join(mdb_dir, u'images')
config_file_path = os.path.join(mdb_dir, u'.config')

config = ConfigObj(defaults)
config_user = ConfigObj(config_file_path)
config.merge(config_user)
config.filename = config_file_path

# # FIXME dont do this here
# if (not os.path.exists(mdb_dir)):
#     os.mkdir(mdb_dir)

config.write()
