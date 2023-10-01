from tensorflow import one_hot
from tqdm import tqdm
import mido
import model
import os
import pickle
import numpy as np

#Constrain it from 94-31, so there are 64 of them!

DATA_FOLDER = "Classical"
BATCH_SIZE = 32
LOAD_DATA = False

ai = model.load_model(stateful=False, batchsize=None)
model.plot_model(ai)
note_distribution = np.full(128, 0)
#region Load data
try:
    if LOAD_DATA == False:raise FileNotFoundError
    with open("data.cache", "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    filepaths = []

    for root, directories, files in os.walk(DATA_FOLDER):
        for filename in files:
            filepath = os.path.join(root, filename)
            filepaths.append(filepath)

    data = []

    for i in tqdm(range(len(filepaths))):
        filepath = filepaths[i]
        notes = []
        for msg in mido.MidiFile(filepath):
            if msg.type == "note_on":
                note_distribution[int(msg.note)] += 1
                notes.append(int(msg.note))
                if len(notes) >= BATCH_SIZE+1:
                    data.append(notes)
                    notes = []
    with open("data.cache", "wb") as file:
        pickle.dump(data, file)
    with open("statestic", "wb") as file:
        pickle.dump(note_distribution, file)
data = np.array(data)

x, y = one_hot(data[:,:-1], 128), one_hot(data[:,1:], 128)
print(x.shape)
print(y.shape)
#endregion


while True:
    ai.fit(x, y)
    model.save_model(ai)