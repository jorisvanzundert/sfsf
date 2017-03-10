import os
import csv
import re
import string
import numpy
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sfsf import sfsf_config
from sfsf import epub_to_txt_parser
from sfsf import txt_pre_processor


class MorePunctuationTokenizer( object ):

    def __call__( self, doc ):
        more_punctuation = string.punctuation + '“”‘’«»'
        return word_tokenize( doc.lower().translate( str.maketrans( "", "", more_punctuation ) ) )


class TrainingDataFactory:

    def __init__( self ):
        self.epub_dir_filenames = os.listdir( sfsf_config.get_epub_dir() )
        self.epub_to_txt_parser = epub_to_txt_parser.EPubToTxtParser()
        self.txt_pre_processor = txt_pre_processor.TxtPreProcessor()

    def get_wpg_data( self, wpg_data_file, cull=50 ):
        with open( os.path.join( sfsf_config.get_data_dir(), wpg_data_file ), 'r', encoding="utf-8" ) as csv_infile:
            csv_reader = csv.reader( csv_infile, delimiter=',', quotechar='"')
            isbn_data = []
            headers = next( csv_reader )
            for row in csv_reader:
                # select NUR, ISBN, Title, Author, Total sales
                isbn_data.append( [ row[0], row[1], row[2], row[3], row[11] ] )
            # sort on total copies sold
            isbn_data.sort( key=lambda x: int( x[4] ), reverse=True )
            top_sellers = isbn_data[:cull]
            bottom_sellers = isbn_data[-cull:]
        return ( top_sellers, bottom_sellers )

    # Finds file name in epub directory matching isbn. This ignores the fact
    # that some files have the same isbn (different print runs, differentiated
    # by a date prefix on the file name), the last file name matching the isbn
    # is returned.
    def lookup_epub_filename( self, isbn ):
        epub_file_name = ''
        for file_name in self.epub_dir_filenames:
            if file_name.endswith( '{i}.epub'.format( i=isbn ) ):
                epub_file_name = file_name
        return os.path.join( sfsf_config.get_epub_dir(), epub_file_name )

    def convert_to_text( self, isbn ):
        text = self.epub_to_txt_parser.narrative_from_epub_to_txt( self.lookup_epub_filename( isbn ) )
        return self.txt_pre_processor.transform( text )

    def sample_epubs( self, isbn_data, sample_size ):
        samples = []
        for isbn_info in isbn_data:
            narrative_text = self.convert_to_text( isbn_info[1] )
            print( isbn_info[1], ':', end=' ' )
            samples.extend( self.sample_string( narrative_text, sample_size ) )
        return samples

    def sample_txts( self, isbn_data, sample_size ):
        samples = []
        for isbn_info in isbn_data:
            txt_file = open( os.path.join( sfsf_config.get_txt_dir(),  '{i}.txt'.format( i=isbn_info[1])  ), 'r' )
            narrative_text = txt_file.read()
            txt_file.close()
            print( isbn_info[1], ':' , end=' ' )
            samples.extend( self.sample_string( narrative_text, sample_size ) )
        return samples

    def sample_string( self, string, sample_size ):
        samples = re.findall( '(?:[^\s]+\s+){{{s}}}'.format( s = sample_size ), string )
        print( '{n} samples extracted'.format( n = len( samples ) ) )
        return samples

    def create( self, wpg_data_file, cull=50, sample_size=1000, source=sfsf_config.EPUB ):
        top_sellers, bottom_sellers = self.get_wpg_data( wpg_data_file, cull )
        if source == sfsf_config.EPUB:
            training_samples_top = self.sample_epubs( top_sellers, sample_size )
            training_samples_bottom = self.sample_epubs( bottom_sellers, sample_size )
        else:
            training_samples_top = self.sample_txts( top_sellers, sample_size )
            training_samples_bottom = self.sample_txts( bottom_sellers, sample_size )
        y_narr = numpy.array( [1] * len( training_samples_top ) + [0] * len( training_samples_bottom ) )
        vect = TfidfVectorizer( tokenizer = MorePunctuationTokenizer() )
        x_tdm = vect.fit_transform( training_samples_top + training_samples_bottom )
        print( 'Created training data', ':' )
        print( 'x shape', ':', x_tdm.shape )
        print( 'y shape', ':', y_narr.shape )
        # TODO: make a nicer return structure
        return { 'x': x_tdm, 'y': y_narr, 'vectorizer': vect }
