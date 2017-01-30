import numpy
from keras.models import Sequential
from keras.layers import Dense

class NoDeepLearningModelError( Exception ):
    def __str__( self ):
        return( "NoDeepLearningModelError" )

class TestingDimensionError( Exception ):
    def __str__( self ):
        return( "TestingDimensionError" )

class DeepLearningModel:

    def __init__( self ):
        self.model = None
        self.x_dim = 0

    def build( self, training_data, batch_size=10, epochs=150 ):
        x_tdm, y_narr = training_data
        x_narr = numpy.array( x_tdm.toarray() )
        self.x_dim = x_narr.shape[1]
        # neurons in hidden layer: a rule of thumb is 2/3 * (input + output)
        neurons_hidden_layer = int( round( ( self.x_dim + 1 ) * 0.66 ) )
        # fix random seed for reproducibility
        seed = 7
        numpy.random.seed( seed )
        # create model
        self.model = Sequential()
        self.model.add( Dense( 12, input_dim=self.x_dim, init='uniform', activation='relu' ) )
        self.model.add( Dense( neurons_hidden_layer, init='uniform', activation='relu' ) )
        self.model.add( Dense( 1, init='uniform', activation='sigmoid' ) )
        # Compile model
        self.model.compile( loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'] )
        # Fit the model
        verbosity = 1
        self.model.fit( x_narr, y_narr, batch_size, epochs, verbosity )
        # evaluate the model
        scores = self.model.evaluate( x_narr, y_narr )
        # print( self.model.metrics_names )
        # print( "%s: %.2f%%" % ( self.model.metrics_names[1], scores[1]*100 ) )
        accuracy = scores[1]*100
        return accuracy

    def predict( self, narr ):
        if self.model != None:
            if self.x_dim == narr.shape[1]:
                # this ignores words not seen before! (Given a large enough corpus this
                # shouldn't be a big problem.)
                predictions = self.model.predict( narr )
                return predictions
            else:
                raise TestingDimensionError
        else:
            raise NoDeepLearningModelError

    def save( self, file_path ):
        raise NotImplementedError

    def load( self, file_path ):
        raise NotImplementedError
