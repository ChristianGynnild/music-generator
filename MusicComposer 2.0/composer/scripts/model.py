import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Softmax, LSTM, InputLayer
from tensorflow.keras import layers, optimizers
from tensorflow import keras
import numpy as np



MODEL_WEIGHTS = 'model_weights'
DICT_SIZE = 72603
EMBEDDING_DIM = 16


def make_model(stateful=False, batch_size=None):
    if stateful == False:batch_size=None

    model = Sequential([
        #InputLayer( input_shape=(batch_size)),# batch_size=batch_size),
        Embedding(DICT_SIZE, EMBEDDING_DIM, name="embedding", batch_size=batch_size),
        Dense(EMBEDDING_DIM, 'relu'),
        LSTM(128, activation='relu', return_sequences=True, stateful=stateful),
        LSTM(128, activation='relu', return_sequences=True, stateful=stateful),
        Dense(128, 'relu'),
        Dense(DICT_SIZE, activation='relu'),
        Softmax()
    ])

    model.compile(
        optimizer=optimizers.Adam(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy()
    )
    return model


def load_model(stateful=False, batchsize=None):
    try:
        model = make_model(stateful, batchsize)
        model.load_weights(MODEL_WEIGHTS)
        return model
    except:
        return make_model(stateful, batchsize)


def save_model(model):
    model.save_weights(MODEL_WEIGHTS)

def plot_model(model):
    keras.utils.plot_model(model, "topology.png", show_shapes=True)

def model_generator(input, certinty=5):
    OUTPUT_SIZE = 72603

    def gen():
        model = load_model(stateful=True, batchsize=1)
        #Can problebly not deal with longer sequences then 1 right now as input!!
        output = model(input)
        print(output.shape)
        #output = np.array(output[0][-1]).reshape((1,1,OUTPUT_SIZE))

        while True:
            highest_index = np.array(output[0]).argmax()
            weights = np.array(output).reshape((OUTPUT_SIZE))
            weights[highest_index] *= certinty
            weights /= np.sum(weights)
            index = np.random.choice(np.arange(OUTPUT_SIZE), p=weights)
            #output = tf.reshape(tf.one_hot(index, OUTPUT_SIZE), (1,1,OUTPUT_SIZE))

            yield index
            output = model.predict([[int(index)]])

    return gen()
