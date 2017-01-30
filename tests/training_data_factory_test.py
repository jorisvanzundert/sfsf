import setup_dev
import unittest
import os
from sfsf import sfsf_config
from sfsf import training_data_factory
import pandas

class TrainingDataFactoryTest( unittest.TestCase ):

    def setUp(self):
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )

    def test_get_wpg_data( self ):
        training_data = training_data_factory.TrainingDataFactory()
        samples_tuple = training_data.get_wpg_data(  'wpg_data.csv', cull=2 )
        csv = pandas.read_csv( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ) )
        smallest_sale = min( csv['totaal afzet'] )
        self.assertEqual( smallest_sale, int( samples_tuple[1][1][4] ) )
        highest_sale = max( csv['totaal afzet'] )
        self.assertEqual( highest_sale, int( samples_tuple[0][0][4] ) )

    def test_sampling( self ):
        isbn_info = [ [ '', 9789023449416, '' ] ]
        training_data = training_data_factory.TrainingDataFactory()
        samples = training_data.sample_texts( isbn_info, 1000 )
        self.assertEqual( 72, len( samples) )

    def test_create_training_data( self ):
        training_data = training_data_factory.TrainingDataFactory()
        training_result = training_data.create( 'wpg_data.csv', 2 )
        self.assertEqual( ( 253, 21627 ), training_result['x'].shape )
        self.assertEqual( ( 253, ), training_result['y'].shape )

if __name__ == '__main__':
    unittest.main()
