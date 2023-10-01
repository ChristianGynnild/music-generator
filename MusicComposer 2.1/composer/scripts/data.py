import mido
import numpy as np
import os
from tqdm import tqdm
import pickle
import composer

DATA_FOLDER = "Classical"
BATCH_SIZE = 65
LOAD_DATA = False
LOAD_DIC = False

files = []

for mainfolder, folders, filenames in os.walk(DATA_FOLDER):
    for filename in filenames:
        files.append(os.path.join(mainfolder,filename))


#region dictionary list
dictionary_list = []


try:
    if LOAD_DIC:raise Exception
    with open("data/chord_list", "rb") as file:
        dictionary_list = pickle.load(file)
except:
    print("Making dictionary list...")
    for i in tqdm(range(len(files))):
        file = files[i]
        midifile = mido.MidiFile(file)

        chord = []
        for msg in midifile:
            if msg.type == "note_on":
                if msg.time == 0 or chord == []:
                    chord.append(msg.note)
                else:
                    instance = tuple(sorted(chord))
                    if instance not in dictionary_list: dictionary_list.append(instance)
                    chord = [msg.note]
            elif msg.time != 0:
                if chord != []:
                    instance = tuple(sorted(chord))
                    if instance not in dictionary_list: dictionary_list.append(instance)
                chord = []
        if chord != []:
            instance = tuple(sorted(chord))
            if instance not in dictionary_list: dictionary_list.append(instance)
    with open("data/chord_list", "wb") as file:
        pickle.dump(dictionary_list, file)

#endregion

#region dictionary
dictionary = {}
for i, chord in enumerate(dictionary_list):
    dictionary[chord] = i

with open("data/chord_dict", "wb") as file:
    pickle.dump(dictionary,file)


#endregion


#region load data
try:
    if LOAD_DATA:raise Exception
    with open("data/dataset", "rb") as file:
        dataset = pickle.load(file)
except:
    dataset = []
    print("Loading files...")
    for i in tqdm(range(len(files))):
        file = files[i]
        midifile = mido.MidiFile(file)
        batch = []
        chord = []
        for msg in midifile:
            if msg.type == "note_on":
                if msg.time == 0 or chord == []:
                    chord.append(msg.note)
                else:
                    batch.append(dictionary[tuple(sorted(chord))])
                    if len(batch) >= BATCH_SIZE:
                        dataset.append(batch)
                        batch = []
                    chord = [msg.note]
            elif msg.time != 0:
                if chord != []:
                    batch.append(dictionary[tuple(sorted(chord))])
                    if len(batch) >= BATCH_SIZE:
                        dataset.append(batch)
                        batch = []
                chord = []

    dataset = np.array(dataset)

    with open("data/dataset", "wb") as file:
        pickle.dump(dataset, file)
#endregion

print(len(dictionary_list))

x = dataset[:,:-1]
y = dataset[:,1:]

with open("data/trainingset", "wb") as file:
    pickle.dump((x,y), file)

#
# for batch in dataset:
#     for chord in batch:
#         print(chord)
#     print("-----------------------")
