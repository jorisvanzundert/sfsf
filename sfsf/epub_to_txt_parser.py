import sys, getopt
import errno
import os.path
import epub
import lxml
import sfsf
from bs4 import BeautifulSoup

class EPubToTxtParser:

    # Epub parsing specific code
    def get_linear_items_data( self, in_file_name ):
        book_items = []
        book = epub.open_epub( in_file_name )
        for item_id, linear in book.opf.spine.itemrefs:
            item = book.get_item( item_id )
            if linear:
                data = book.read_item( item )
                book_items.append( data )
        return book_items

    def get_narrative( self, linear_items_data ):
        avg_len = 0
        count = 0
        for data in linear_items_data:
            count += 1
            avg_len = ( ( avg_len * ( count - 1 ) ) + len( data ) ) / count
        book_narrative = [ data for data in linear_items_data if len(data) >= avg_len ]
        return book_narrative

    def extract_paragraph_text( self, book_narrative ):
        paragraph_text = ''
        for data in book_narrative:
            soup = BeautifulSoup( data, "lxml" )
            paragraphs = soup.find_all( 'p' )
            for paragraph in paragraphs:
                paragraph_text += ( paragraph.get_text() + '\n' )
        return paragraph_text

    def narrative_from_epub_to_txt( self, in_file_name ):
        if os.path.isfile( in_file_name ):
            book_items = self.get_linear_items_data( in_file_name )
            book_narrative = self.get_narrative( book_items )
            paragraph_text = self.extract_paragraph_text( book_narrative )
            return( paragraph_text )
        else:
            raise FileNotFoundError( errno.ENOENT, os.strerror( errno.ENOENT ), in_file_name )


# Command line usage stuff
def print_usage_and_exit():
    print( "Usage: %s -i epub_file_in -o txt_file_out" % sys.argv[ 0 ] )
    sys.exit( 2 )

def parse_opts( opts ):
    in_file_name, out_file_name = None, None
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

    try:
        parser = EPubToTxtParser()
        narrative_text = parser.narrative_from_epub_to_txt( in_file_name )
        if( out_file_name != None ):
            with open( out_file_name, "w" ) as out_file:
                out_file.write( narrative_text )
            out_file.close()
        else:
            print( narrative_text )
    except FileNotFoundError:
        print( "File not found: {file_name}".format( file_name = in_file_name ) )
