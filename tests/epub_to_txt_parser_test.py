import setup_dev
import unittest
import os
from sfsf import epub_to_txt_parser
from sfsf import sfsf_config

class EpubToTxtParserTest( unittest.TestCase ):

    def setUp(self):
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )

    def test_get_linear_items_data( self ):
        parser = epub_to_txt_parser.EPubToTxtParser()
        dir_path = os.path.dirname( os.path.realpath(__file__) )
        items = []
        path_to_nantas = os.path.join( sfsf_config.get_data_dir(), 'epub/9789460422515.epub' )
        items = parser.get_linear_items_data( path_to_nantas )
        self.assertEqual( len( items ), 5 )

    def test_get_narrative( self ):
        parser = epub_to_txt_parser.EPubToTxtParser()
        dir_path = os.path.dirname( os.path.realpath(__file__) )
        items = []
        path_to_nantas = os.path.join( sfsf_config.get_data_dir(), 'epub/9789460422515.epub' )
        items = parser.get_linear_items_data( path_to_nantas )
        narrative = parser.get_narrative( items )
        self.assertEqual( len( narrative ), 3 )

    def test_extract_paragraph_text( self ):
        parser = epub_to_txt_parser.EPubToTxtParser()
        items = []
        items.append( '<docu><p>hello</p><p>world</p></docu>' )
        text = parser.extract_paragraph_text( items )
        expected = 'hello\nworld\n'
        self.assertEqual( text, expected )

if __name__ == '__main__':
    unittest.main()
