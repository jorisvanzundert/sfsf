import setup_dev
import unittest
from sfsf import txt_pre_processor

class TxtPreProcessorTest( unittest.TestCase ):

    def test_txt_pre_processor( self ):
        pre_processor = txt_pre_processor.TxtPreProcessor()
        result = pre_processor.transform( "Iets[8] [7]met [8] pagina num[9]mers" )
        self.assertEqual( "Iets met  pagina nummers", result )

if __name__ == '__main__':
    unittest.main()
