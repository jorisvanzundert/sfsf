from sfsf import sfsf_config
from sfsf import training_data_factory
from sfsf import deep_learning_model
from datetime import datetime

# main
training_factory = training_data_factory.TrainingDataFactory()
training_data = factory.create_by_indices( 'wpg_data.csv', (1,52,-600,-549), sample_size=5000, source=sfsf_config.TXT  )
vectorizer = training_data[ 'vectorizer' ]
testing_top, testing_bottom = training_factory.get_top_bottom_by_indices( 'wpg_data.csv', (53,58,-608,-603) )
testing_samples_top = training_factory.sample_txts( testing_top, 5000 )
testing_samples_bottom = training_factory.sample_txts( testing_bottom, 5000 )
testing_tdm_top = vectorizer.transform( testing_samples_top )
model = deep_learning_model.DeepLearningModel()
# training_data, batch_size, epochs
accuracy = model.build( ( training_data['x'], training_data['y'] ), 10, 5 )
model.save( 'sfsf_deeplearning_model_{d}.h5'.format( d=datetime.now().strft( '%Y%m%d_%H%M' ) )
predictions = model.predict( numpy.array( testing_tdm_top.toarray() ) )
for idx, prediction in enumerate( predictions ):
    print( prediction[0] )
