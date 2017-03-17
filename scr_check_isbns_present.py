import csv
import os

files_epub_dir = [ f for f in os.listdir( 'Bruna-BezigeBij' ) if os.path.isfile( os.path.join( 'Bruna-BezigeBij', f ) ) ]

csv_file = open( 'Bruna-BezigeBij/wpg_data.csv', 'r', encoding='utf-8' )
csv_reader = csv.reader( csv_file, delimiter=',', quotechar='"' )
headers = next( csv_reader )
for row in csv_reader:
    isbn = row[1]
    epubs = []
    for file_name in files_epub_dir:
        if isbn in file_name:
            epubs.append( file_name )
    if len( epubs ) > 1:
        print( isbn, 'more than 1 found: ', len( epubs ) )
        for epub in epubs:
            print( '\t', epub )
    if len( epubs ) == 0 :
        print( isbn, 'not found' )
