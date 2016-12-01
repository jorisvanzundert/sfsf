import sys, getopt
import os.path
import epub
from bs4 import BeautifulSoup

# Epub parsing specific code
def get_linear_items_data( in_file_name ):
    book_items = []
    book = epub.open_epub( in_file_name )
    for item_id, linear in book.opf.spine.itemrefs:
        item = book.get_item( item_id )
        if linear:
            data = book.read_item( item )
            book_items.append( data )
    return book_items

def get_narrative( linear_items_data ):
    avg_len = 0
    count = 0
    for data in linear_items_data:
        count += 1
        avg_len = ( ( avg_len * ( count - 1 ) ) + len( data ) ) / count
    book_narrative = [ data for data in linear_items_data if len(data) >= avg_len ]
    return book_narrative

def extract_paragraph_text( book_narrative ):
    paragraph_text = ''
    for data in book_narrative:
        soup = BeautifulSoup( data, "lxml" )
        paragraphs = soup.find_all( 'p' )
        for paragraph in paragraphs:
            paragraph_text += ( paragraph.get_text() + '\n' )
    return paragraph_text

# Command line usage stuff
def print_usage_and_exit():
    print( "Usage: %s -i epub_file_in -o txt_file_out" % sys.argv[ 0 ] )
    sys.exit( 2 )

def parse_opts( opts ):
    for o, a in opts:
        if o == '-i':
            in_file_name = a
        elif o == '-o':
            out_file_name = a
    return ( in_file_name, out_file_name )

# Main
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:")
        assert( len(opts) != 0 )
        in_file_name, out_file_name = parse_opts( opts )
    except getopt.GetoptError as e:
        print( str( e ) )
        print_usage_and_exit()
    except AssertionError:
        print_usage_and_exit()

    if os.path.isfile( in_file_name ):
        book_items = get_linear_items_data( in_file_name )
        book_narrative = get_narrative( book_items )
        paragraph_text = extract_paragraph_text( book_narrative )
        with open( out_file_name, "w" ) as out_file:
            out_file.write( paragraph_text )
        out_file.close()
