from sfsf import sfsf_config
from sfsf import training_data_factory
from sfsf import deep_learning_model
from datetime import datetime
import numpy
import pickle

training_factory = training_data_factory.TrainingDataFactory()
training_data = pickle.load( open( 'sfsf_training_data.pickle', 'rb' ) )
vectorizer = training_data[ 'vectorizer' ]
testing_top, testing_bottom = training_factory.get_top_bottom_by_indices( 'wpg_data.csv', (53,58,-608,-603) )
testing_samples_top = training_factory.sample_txts( testing_top, 5000 )
testing_samples_bottom = training_factory.sample_txts( testing_bottom, 5000 )
testing_tdm_top = vectorizer.transform( testing_samples_top )
testing_tdm_bottom = vectorizer.transform( testing_samples_bottom )
model = deep_learning_model.DeepLearningModel()
# training_data, batch_size, epochs
accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
model.save( 'sfsf_deeplearning_model_{d}'.format( d=datetime.now().strftime( '%Y%m%d_%H%M' ) ) )
predictions = model.predict( numpy.array( testing_tdm_bottom.toarray() ) )
for idx, prediction in enumerate( predictions ):
    print( prediction[0] )
