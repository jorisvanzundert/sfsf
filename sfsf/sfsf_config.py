import os

PRODUCTION = 'production'
DEVELOPMENT = 'test'
ENVIRONMENT = PRODUCTION

def set_env( env=PRODUCTION ):
    global ENVIRONMENT
    ENVIRONMENT = env

def get_data_dir():
    path_to_here = os.path.dirname( os.path.abspath( __file__ ) )
    if ENVIRONMENT == DEVELOPMENT:
        data_dir = os.path.join(  path_to_here, '../data/{t}'.format( t=DEVELOPMENT ) )
    else:
        data_dir = os.path.join( path_to_here, '../data/{p}'.format( p=PRODUCTION ) )
    return data_dir
