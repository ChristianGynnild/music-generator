from midiutil import MIDIFile
import io
from pygame import mixer, time
import pygame
import random
import numpy as np
import os
import mido
from collections import defaultdict
from tqdm import tqdm
import pickle

RELOAD = False


#region load data
try:
    def placeholder():
        return 0

    if RELOAD:raise Exception
    with open("../data/stats.cache", "rb") as file:
        stats = pickle.load(file)
except Exception as e:
    print(e)

    def placeholder():
        return 0

    stats = defaultdict(placeholder)
    files = []
    DATA_PATH = "../Classical"
    for folder_root, folders, filenames in os.walk(DATA_PATH):
        for filename in filenames:
            file = os.path.join(folder_root, filename)
            files.append(file)

    for i in tqdm(range(len(files))):
        file = files[i]
        midi = mido.MidiFile(file)
        chord = []
        for msg in midi:
            if msg.type == "note_on":
                if msg.time == 0 or chord == []:
                    if msg.note not in chord:chord.append(msg.note)
                else:
                    key = tuple(sorted(chord))
                    if key != (): stats[key] += 1
                    chord = []
                    chord.append(msg.note)
        key = tuple(sorted(chord))
        if key != (): stats[key] += 1
    with open("../data/stats.cache", "wb") as file:
        pickle.dump(stats,file)
#endregion


stats = sorted(stats.items(), key=lambda x:x[1])

print((stats)[0])
for i, item in enumerate(stats):
    print(f"{len(stats)-i}: {item}")

print(len(stats))
