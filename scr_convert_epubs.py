import csv
import os
import traceback
from sfsf import sfsf_config
from sfsf import epub_to_txt_parser
from sfsf import txt_pre_processor
from sfsf import training_data_factory

# sfsf_config.set_env( sfsf_config.DEVELOPMENT )

with open( os.path.join( sfsf_config.get_data_dir(), 'wpg_data.csv' ), 'r', encoding="utf-8" ) as csv_infile:
    training_data_fact = training_data_factory.TrainingDataFactory()
    parser = epub_to_txt_parser.EPubToTxtParser()
    text_preprocessor = txt_pre_processor.TxtPreProcessor()
    csv_reader = csv.reader( csv_infile, delimiter=',', quotechar='"')
    tmp_txt_files = []
    headers = next( csv_reader )    
    for row in csv_reader:
        try:
            text = parser.narrative_from_epub_to_txt( training_data_fact.lookup_epub_filename( row[1] ) )
            text = text_preprocessor.transform( text )
            tmp_txt_file_name = os.path.join( sfsf_config.get_txt_dir(), '{i}.txt'.format( i=row[1] ) )
            tmp_txt_files.append( tmp_txt_file_name )
            txt_file = open( tmp_txt_file_name, 'w', encoding='utf8' )
            txt_file.write( text )
            txt_file.close()
            print( row[1], end=' ' )
        except:
            print( '\n', 'Caught an error for {r}'.format( r=row[1] ), '\n', traceback.format_exc() )
