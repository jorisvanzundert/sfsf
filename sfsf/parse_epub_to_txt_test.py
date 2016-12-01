import unittest
import os
import parse_epub_to_txt

class TestParseEpubToTxt( unittest.TestCase ):

    def test_get_linear_items_data( self ):
        dir_path = os.path.dirname( os.path.realpath(__file__) )
        items = []
        items = parse_epub_to_txt.get_linear_items_data( dir_path + '/../test_data/nantas.epub' )
        self.assertEqual( len( items ), 5 )

    def test_get_narrative( self ):
        dir_path = os.path.dirname( os.path.realpath(__file__) )
        items = []
        items = parse_epub_to_txt.get_linear_items_data( dir_path + '/../test_data/nantas.epub' )
        narrative = parse_epub_to_txt.get_narrative( items )
        self.assertEqual( len( narrative ), 3 )

    def test_extract_paragraph_text( self ):
        items = []
        items.append( '<docu><p>hello</p><p>world</p></docu>' )
        text = parse_epub_to_txt.extract_paragraph_text( items )
        expected = 'hello\nworld\n'
        self.assertEqual( text, expected )

if __name__ == '__main__':
    unittest.main()
