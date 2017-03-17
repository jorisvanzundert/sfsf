import csv
import os
import re
import traceback
from sfsf import sfsf_config

# sfsf_config.set_env( sfsf_config.DEVELOPMENT )

def print_info( items, message ):
    file_sizes = []
    for item in items:
        file_size = os.path.getsize( os.path.join( sfsf_config.get_txt_dir(), '{i}.txt'.format( i=item[1] ) ) )
        file_sizes.append( [ item[1], item[4], file_size, item[2] ] )

    file_sizes.sort( key=lambda x: int( x[2] ) )
    print( '-------', message, '------' )
    for item in file_sizes:
        txt_file = open( os.path.join( sfsf_config.get_txt_dir(), '{i}.txt'.format( i=item[0] ) ), 'r', encoding="utf-8" )
        nwords = len( re.findall( '\s+', txt_file.read() ) )
        print( item[0], item[1], round(item[2]/1024), nwords, item[3], sep='\t' )

# main
with open( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ), 'r', encoding="utf-8" ) as csv_infile:
    csv_reader = csv.reader( csv_infile, delimiter=',', quotechar='"')
    tmp_txt_files = []
    isbn_data = []
    headers = next( csv_reader )
    for row in csv_reader:
        # select NUR, ISBN, Title, Author, Total sales
        isbn_data.append( [ row[0], row[1], row[2], row[3], row[11] ] )
    # sort on total copies sold
    isbn_data.sort( key=lambda x: int( x[4] ), reverse=True )
    top_sellers = isbn_data[:100]
    print_info( top_sellers, 'Top sellers: isbn, afzet, Kb, word count, title' )
    bottom_sellers = isbn_data[-600:-500]
    print_info( bottom_sellers, 'Bottom sellers: isbn, afzet, Kb, word count, title' )

