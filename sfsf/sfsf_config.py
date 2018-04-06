import os

PRODUCTION = 'merged-corpus'
DEVELOPMENT = 'test'
ENVIRONMENT = PRODUCTION
EPUB = 'epub'
EPUB_DIRNAME = EPUB
TXT = 'txt'
TXT_DIRNAME = TXT

def set_env( env=PRODUCTION ):
    global ENVIRONMENT
    ENVIRONMENT = env

def get_data_dir():
    path_to_here = os.path.dirname( os.path.abspath( __file__ ) )
    if ENVIRONMENT == DEVELOPMENT:
        data_dir = os.path.join(  path_to_here, '../data/{t}'.format( t=DEVELOPMENT ) )
    else:
        data_dir = os.path.join( path_to_here, '../../docker_volume/{p}'.format( p=PRODUCTION ) )
    return data_dir

def get_epub_dir():
    return os.path.join( get_data_dir(), EPUB_DIRNAME )

def get_txt_dir():
    return os.path.join( get_data_dir(), TXT_DIRNAME )
