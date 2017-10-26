from sfsf import sfsf_config
from sfsf import training_data_factory
from sfsf import deep_learning_model
from datetime import datetime
from random import shuffle
import numpy
import csv
import pickle

def report( report_row, csv_writer ):
    print( '\t'.join( report_row ) )
    csv_writer.writerow( report_row )

def do_predict(train_num, test_num, total_size, iterations):
    train_size = {
        "top": train_num,
        "bottom": train_num
    }
    test_size = {
        "top": test_num,
        "bottom": test_num
    }
    wpg_data_file = 'wpg_data.csv'
    for iteration in range(1, iterations+1):
            print("Train/test ({train}/{test}) sampled from {total} iteration {curr_iter} of {num_iters}".format(train=train_num, test=test_num, total=total_size, curr_iter=iteration, num_iters=iterations))
            train_sample, test_sample = do_sample(wpg_data_file, train_size, test_size, total_size)
            do_train(train_sample)
            do_test(test_sample, train_num, test_num, total_size, iteration)

def do_sample(wpg_data_file, train_size, test_size, total_size):
    training_factory = training_data_factory.TrainingDataFactory()
    isbn_data = training_factory.get_isbn_data( wpg_data_file ) # returns data sorted by sales
    top_data = isbn_data[:total_size]
    bottom_data = isbn_data[-total_size:]
    shuffle(top_data)
    shuffle(bottom_data)
    train_sample = {
        "top": top_data[:train_size["top"]],
        "bottom": bottom_data[:train_size["bottom"]],
    }
    test_sample = {
        "top": top_data[-test_size["top"]:],
        "bottom": bottom_data[-test_size["bottom"]:]
    }
    return train_sample, test_sample

def do_train(train_sample):
    training_factory = training_data_factory.TrainingDataFactory()
    training_data = training_factory.create_by_sample( 'wpg_data.csv', train_sample["top"], train_sample["bottom"], sample_size=5000, source=sfsf_config.TXT  )
    pickle.dump( training_data, open( 'sfsf_training_data.pickle', 'wb' ) )

# main
def do_test(test_sample, train_size, test_size, total_size, iteration):
    # Test training data and predict
    training_factory = training_data_factory.TrainingDataFactory()
    training_data = pickle.load( open( 'sfsf_training_data.pickle', 'rb' ) )
    vectorizer = training_data[ 'vectorizer' ]
    testing_data_top = training_factory.sample_txts( test_sample["top"], 5000 )
    testing_data_bottom = training_factory.sample_txts( test_sample["bottom"], 5000 )
    isbns_top = [ tuple[0] for tuple in testing_data_top for sample in tuple[1] ]
    isbns_bottom = [ tuple[0] for tuple in testing_data_bottom for sample in tuple[1] ]
    testing_tdm_top = vectorizer.transform( [ sample for tuple in testing_data_top for sample in tuple[1] ] )
    testing_tdm_bottom = vectorizer.transform( [ sample for tuple in testing_data_bottom for sample in tuple[1] ] )
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
        predictions_bottom.append( ( isbns_bottom[idx], prediction[0] ) )

    # reporting
    report_file_name = 'report-total-{total}-train-{train}-test-{test}-iteration-{i}-date-{d}.csv'.format( total=total_size, train=train_size, test=test_size, i=iteration, d=datetime.now().strftime( '%Y%m%d_%H%M' ) )
    report_file = open( report_file_name, 'w', encoding='utf8' )
    csv_writer = csv.writer( report_file, delimiter=',' )
    training_factory = training_data_factory.TrainingDataFactory()
    isbn_data = training_factory.get_isbn_data( 'wpg_data.csv' )
    headers = ['deep_learning_data_type', 'NUR', 'ISBN', 'title', 'author', 'total sold', 'prediction' ]
    csv_writer.writerow( headers )
    print( '\t'.join( headers ) )
    training_isbns_reported = []
    # combine training data y and isbns
    for idx, item in enumerate( training_data['y'] ):
        if not training_data['isbns'][idx] in training_isbns_reported:
            report_row = []
            # 1 is top, 0 is flop
            if item == 1:
                report_row.append( 'training_top' )
            else:
                report_row.append( 'training_bottom' )
            #isbn: find the data
            isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_inf[1]==training_data['isbns'][idx] )
            report_row.extend( isbn_info )
            report_row.append( 'NA' )
            report( report_row, csv_writer )
            training_isbns_reported.append( training_data['isbns'][idx] )
    for prediction in predictions_top:
        report_row = []
        report_row.append( 'testing_top' )
        #isbn: find the data
        isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_inf[1]==prediction[0] )
        report_row.extend( isbn_info )
        report_row.append( str( prediction[1] ) )
        report( report_row, csv_writer )
    for prediction in predictions_bottom:
        report_row = []
        report_row.append( 'testing_bottom' )
        #isbn: find the data
        isbn_info = next( isbn_inf for isbn_inf in isbn_data if isbn_inf[1]==prediction[0] )
        report_row.extend( isbn_info )
        report_row.append( str( prediction[1] ) )
        report( report_row, csv_writer )
    report_file.close()

if __name__ == "__main__":
    total_top_bottom = 120
    iterations = 10
    train_size = 20
    test_size = 20
    do_predict(train_size, test_size, total_top_bottom, iterations)
    train_size = 50
    do_predict(train_size, test_size, total_top_bottom, iterations)
    train_size = 100
    do_predict(train_size, test_size, total_top_bottom, iterations)
    #do_predict(50, 10)
