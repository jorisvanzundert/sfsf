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

    def get_wpg_data( self, wpg_data_file, cull=50 ):
        with open( os.path.join( sfsf_config.get_data_dir(), wpg_data_file), 'r', encoding="utf-8" ) as csv_infile:
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

    def sample_texts( self, isbn_data, sample_size ):
        samples = []
        parser = epub_to_txt_parser.EPubToTxtParser()
        pre_processor = txt_pre_processor.TxtPreProcessor()
        for isbn_info in isbn_data:
            narrative_text = parser.narrative_from_epub_to_txt( os.path.join( sfsf_config.get_data_dir(), 'epub/{i}.epub'.format( i = isbn_info[1] ) ) )
            narrative_text = pre_processor.transform( narrative_text )
            new_samples = re.findall( '(?:[^\s]+\s+){{{s}}}'.format( s = sample_size ), narrative_text )
            samples.extend( new_samples )
            print( isbn_info[1], ": ", "{n} samples added".format( n = len( new_samples ) ) )
        return samples

    def create( self, wpg_data_file, cull=50, sample_size=1000 ):
        top_sellers, bottom_sellers = self.get_wpg_data( wpg_data_file, cull )
        training_samples_top = self.sample_texts( top_sellers, sample_size )
        training_samples_bottom = self.sample_texts( bottom_sellers, sample_size )
        y_narr = numpy.array( [1] * len( training_samples_top ) + [0] * len( training_samples_bottom ) )
        vect = TfidfVectorizer( tokenizer = MorePunctuationTokenizer() )
        x_tdm = vect.fit_transform( training_samples_top + training_samples_bottom )
        print( "Created training data:")
        print( "x shape: ", x_tdm.shape )
        print( "y shape: ", y_narr.shape )
        # TODO: make a nicer return structure
        return { 'x': x_tdm, 'y': y_narr, 'vectorizer': vect }
