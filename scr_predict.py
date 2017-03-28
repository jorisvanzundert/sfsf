from sfsf import sfsf_config
from sfsf import training_data_factory
from sfsf import deep_learning_model
from datetime import datetime
import numpy
import pickle

def report( report_row, csv_writer ):
    print( '\t'.join( report_row ) )
    csv_writer.writerow( report_row )

# main
# Test training data and predict
training_factory = training_data_factory.TrainingDataFactory()
training_data = pickle.load( open( 'sfsf_training_data.pickle', 'rb' ) )
vectorizer = training_data[ 'vectorizer' ]
testing_top, testing_bottom = training_factory.get_top_bottom_by_indices( 'wpg_data.csv', (53,58,-608,-603) )
testing_data_top = training_factory.sample_txts( testing_top, 5000 )
testing_data_bottom = training_factory.sample_txts( testing_bottom, 5000 )
isbns_top = [ tuple[0] for tuple in testing_data_top for sample in tuple[1]
isbns_bottom = [ tuple[0] for tuple in testing_data_bottom for sample in tuple[1]
testing_tdm_top = vectorizer.transform( [ sample for tuple in testing_data_top for sample in tuple[1] )
testing_tdm_bottom = vectorizer.transform( [ sample for tuple in testing_data_bottom for sample in tuple[1] )
model = deep_learning_model.DeepLearningModel()
# training_data, batch_size, epochs
accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
model.save( 'sfsf_deeplearning_model_{d}'.format( d=datetime.now().strftime( '%Y%m%d_%H%M' ) ) )
predictions = model.predict( numpy.array( testing_tdm_top.toarray() ) )
predictions_top = []
predictions_bottom = []
for idx, prediction in enumerate( predictions ):
    predictions_top.append( ( isbns_top[idx], prediction[0] ) )
predictions = model.predict( numpy.array( testing_tdm_bottom.toarray() ) )
for idx, prediction in enumerate( predictions ):
    predictions_bottom.append( ( isbns_top[idx], prediction[0] ) )

# reporting
report_file_name = 'report_{d}.csv'.format( d=datetime.now().strftime( '%Y%m%d_%H%M' ) )
report_file = open( report_file_name, 'w', encoding='utf8' )
csv_writer = csv.writer( report_file, delimiter=',' )
training_factory = training_data_factory.TrainingDataFactory()
isbn_data = training_factory.get_isbn_data( 'wpg_data.csv' )
headers = ['deep_learning_data_type', 'NUR', 'ISBN', 'title', 'author', 'total sold', 'prediction' ]
csv_writer.writerow( headers )
print( '\t'.join( headers ) )
# combine training data y and isbns
for idx, item in enumerate( training_data['y'] ):
    report_row = []
    # 1 is top, 0 is flop
    if item == 1:
        report_row.append( 'training_top' )
    else:
        report_row.append( 'training_bottom' )
    #isbn: find the data
    isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_data[1]==training_data['isbns'][idx] )
    report_row.append( isbn_info )
    report_row.append( 'NA' )
    report( report_row, csv_writer )
for prediction in predictions_top:
    report_row = []
    report_row.append( 'testing_top' )
    #isbn: find the data
    isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_data[1]==prediction[0] )
    report_row.append( isbn_info )
    report_row.append( prediction[1] )
    report( report_row, csv_writer )
for prediction in predictions_bottom:
    report_row = []
    report_row.append( 'testing_bottom' )
    #isbn: find the data
    isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_data[1]==prediction[0] )
    report_row.append( isbn_info )
    report_row.append( prediction[1] )
    report( report_row, csv_writer )
