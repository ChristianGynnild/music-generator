#!/home/christian/Interpeters/MusicComposer/bin/python
import os
import composer.scripts.model as model
from tensorflow import one_hot
import numpy as np
from midiutil import MIDIFile
import io
import pickle
from pygame import mixer


INPUT_SIZE = 72603#71525

data = [[58]]
data = np.array(data)


ai_gen = model.model_generator(data, 15)

# while True:
#     print(ai_gen.__next__())


const = 1
DURATION = 1 * const  # In beats
TEMPO = 60 * 4 /const   # In BPM
VOLUME = 100  # 0-127, as per the MIDI standard
mixer.init(44100, -16, 1, 64)

with open("data/chord_list", "rb") as file:
    chord_list = pickle.load(file)



count = 0
while True:
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, TEMPO)

    lowest_note = 128
    highest_note = 0
    for i in range(256):
        try:
            chord = chord_list[ai_gen.__next__()]
            for note in chord:
                MyMIDI.addNote(0, 0, note, i, DURATION, VOLUME)
        except IndexError:
            pass

        count += 1

    buf = io.BytesIO()
    MyMIDI.writeFile(buf)
    buf = io.BytesIO(buf.getbuffer())

    while mixer.music.get_busy():
        pass

    mixer.music.load(buf)
    mixer.music.play()


