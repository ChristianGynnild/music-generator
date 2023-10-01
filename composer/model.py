import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from tensorflow import one_hot
#from tensorflow.keras.layers.experimental.preprocessing import CategoryEncoding

MODEL_WEIGHTS = 'model_weights'

def make_model(stateful=False, batch_size=None):
    #batch_size = None
    #if stateful:batch_size=batchsize


    input = keras.Input(shape=(batch_size, 128), name="input_note", batch_size=batch_size)
    x = layers.LSTM(128, activation='relu', return_sequences=True, stateful=stateful)(input)
    x = layers.LSTM(128, activation='relu', return_sequences=True, stateful=stateful)(x)
    x = layers.Dense(128, 'relu')(x)
    x = layers.Dense(128, 'relu')(x)
    output = layers.Softmax()(x)

    model = keras.Model(
        inputs=[input],
        outputs=[output],
    )

    model.compile(
\
        optimizer=keras.optimizers.Adam(),
        loss=[tf.keras.losses.CategoricalCrossentropy()]
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
    def gen():
        model = load_model(stateful=True, batchsize=1)

        output = model(input)
        output = np.array(output[0][-1]).reshape((1,1,128))

        while True:
            highest_index = np.array(output[0]).argmax()
            weights = np.array(output).reshape((128))
            weights[highest_index] *= certinty
            weights /= np.sum(weights)
            index = np.random.choice(np.arange(128), p=weights)
            output = tf.reshape(tf.one_hot(index, 128), (1,1,128))

            yield index
            output = model(output)

    return gen()
