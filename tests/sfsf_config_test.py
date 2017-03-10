import setup_dev
import os
import unittest
from sfsf import sfsf_config

class SFSFConfigTest( unittest.TestCase ):

    def setUp(self):
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )

    def test_config( self ):
        self.assertEqual( 'txt', sfsf_config.TXT )
        self.assertEqual( 'epub', sfsf_config.EPUB )
        self.assertEqual( 'production', sfsf_config.PRODUCTION )
        self.assertEqual( 'test', sfsf_config.DEVELOPMENT )
        path_to_here = os.path.abspath( os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), os.pardir ) )
        path_to_test = os.path.join( path_to_here, 'sfsf/../data/test' )
        path_to_data = os.path.join( path_to_here, 'sfsf/../data/production' )
        path_to_test_epub = os.path.join( path_to_here, 'sfsf/../data/test/epub' )
        path_to_test_txt = os.path.join( path_to_here, 'sfsf/../data/test/txt' )
        self.assertEqual( path_to_test, sfsf_config.get_data_dir() )
        sfsf_config.set_env( sfsf_config.PRODUCTION )
        self.assertEqual( path_to_data, sfsf_config.get_data_dir() )
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )
        self.assertEqual( path_to_test, sfsf_config.get_data_dir() )
        self.assertEqual( path_to_test_epub, sfsf_config.get_epub_dir() )
        self.assertEqual( path_to_test_txt, sfsf_config.get_txt_dir() )

if __name__ == '__main__':
    unittest.main()
