from composer.app import model
import pickle

BATCH_SIZE = 32

ai = model.load_model(stateful=False, batchsize=None)
model.plot_model(ai)

with open("data/trainingset", "rb") as file:
    x, y = pickle.load(file)

while True:
    ai.fit(x, y)
    model.save_model(ai)