import setup_dev
import csv
import unittest
import os
from sfsf import sfsf_config
from sfsf import epub_to_txt_parser
from sfsf import txt_pre_processor
from sfsf import training_data_factory
import pandas

class TrainingDataFactoryTest( unittest.TestCase ):

    def setUp(self):
        sfsf_config.set_env( sfsf_config.DEVELOPMENT )

    def test_get_top_bottom( self ):
        training_data = training_data_factory.TrainingDataFactory()
        samples_tuple = training_data.get_top_bottom( 'wpg_data.csv', cull=2 )
        csv = pandas.read_csv( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ) )
        smallest_sale = min( csv['totaal afzet'] )
        self.assertEqual( smallest_sale, int( samples_tuple[1][1][4] ) )
        highest_sale = max( csv['totaal afzet'] )
        self.assertEqual( highest_sale, int( samples_tuple[0][0][4] ) )

    def test_get_top_bottom_indices( self ):
        training_data = training_data_factory.TrainingDataFactory()
        samples_tuple = training_data.get_top_bottom_by_indices( 'wpg_data.csv', (0,2,-2,None) )
        csv = pandas.read_csv( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ) )
        smallest_sale = min( csv['totaal afzet'] )
        self.assertEqual( smallest_sale, int( samples_tuple[1][1][4] ) )
        highest_sale = max( csv['totaal afzet'] )
        self.assertEqual( highest_sale, int( samples_tuple[0][0][4] ) )

    def test_file_name_lookup( self ):
        training_data = training_data_factory.TrainingDataFactory()
        assert( training_data.lookup_epub_filename( '9789044964264' ).endswith( '20160113113032_9789044964264.epub' ) )
        # one should be returned in the case of multiples, don't care
        # which one.
        any_which = lambda file_name: file_name.endswith( '20150602093137_9789023449416.epub' ) or file_name.endswith( '20160113113032_9789023449416.epub' )
        result = training_data.lookup_epub_filename( '9789023449416' )
        assert( any_which( result ) )

    def test_sampling( self ):
        isbn_info = [ [ '', 9789023449416, '' ] ]
        training_data = training_data_factory.TrainingDataFactory()
        samples = training_data.sample_epubs( isbn_info, 1000 )
        self.assertEqual( 72, len( samples) )

    def test_create_training_data( self ):
        training_data = training_data_factory.TrainingDataFactory()
        training_result = training_data.create( 'wpg_data.csv', 2 )
        self.assertEqual( ( 253, 21627 ), training_result['x'].shape )
        self.assertEqual( ( 253, ), training_result['y'].shape )

    def test_create_training_data_from_txt( self ):
        training_data_fact = training_data_factory.TrainingDataFactory()
        parser = epub_to_txt_parser.EPubToTxtParser()
        text_preprocessor = txt_pre_processor.TxtPreProcessor()
        with open( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ), 'r', encoding="utf-8" ) as csv_infile:
            csv_reader = csv.reader( csv_infile, delimiter=',', quotechar='"')
            tmp_txt_files = []
            headers = next( csv_reader )
            for row in csv_reader:
                text = parser.narrative_from_epub_to_txt( training_data_fact.lookup_epub_filename( row[1] ) )
                text = text_preprocessor.transform( text )
                tmp_txt_file_name = os.path.join( sfsf_config.get_txt_dir(), '{i}.txt'.format( i=row[1] ) )
                tmp_txt_files.append( tmp_txt_file_name )
                txt_file = open( tmp_txt_file_name, 'w', encoding='utf-8' )
                txt_file.write( text )
                txt_file.close()
                print( row[1] )
        training_result = training_data_fact.create( 'wpg_data.csv', 2, source=sfsf_config.TXT )
        for file_name in tmp_txt_files:
            os.remove( file_name )
        self.assertEqual( ( 253, 21627 ), training_result['x'].shape )
        self.assertEqual( ( 253, ), training_result['y'].shape )

if __name__ == '__main__':
    unittest.main()
