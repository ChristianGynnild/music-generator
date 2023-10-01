import ast
import pickle
from midiutil import MIDIFile
import io
from pygame import mixer, time
import pygame
import random
import numpy as np
import composer

with open("data/dataset", "rb") as file:
    data = pickle.load(file)

with open("data/chord_list", "rb") as file:
    chord_list = pickle.load(file)

np.random.shuffle(data)


DURATION = 0.8    # In beats
TEMPO = 60 * 6   # In BPM
VOLUME = 100  # 0-127, as per the MIDI standard

pygame.mixer.init(44100, -16, 1, 64)


for batch in data:
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, TEMPO)

    for i, chord in enumerate(batch):
        for pitch in chord_list[chord]:
            #print(pitch)
            MyMIDI.addNote(0, 0, int(pitch), i, DURATION, VOLUME)

    buf = io.BytesIO()
    MyMIDI.writeFile(buf)
    buf = io.BytesIO(buf.getbuffer())

    while mixer.music.get_busy():
        pass

    mixer.music.load(buf)
    mixer.music.play()

