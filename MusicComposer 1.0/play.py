#!/home/christian/Interpeters/MusicComposer/bin/python
import os
import model
from tensorflow import one_hot
import numpy as np
import pickle
from midiutil import MIDIFile
import io

from pygame import mixer, time
import pygame
import random

os.chdir("/home/christian/Projects/PycharmProjects/MusicComposer/MusicComposer 1.0")
HIGHEST_NOTE = 85
LOWEST_NOTE = 0
MAKING_MIDI = True

data = [58]
data = np.array((one_hot(data, 128))).reshape((1,1,128))
ai_gen = model.model_generator(data, 3.5)

const = 1
DURATION = 1 * const  # In beats
TEMPO = 60 * 8 /const   # In BPM
VOLUME = 100  # 0-127, as per the MIDI standard
mixer.init(44100, -16, 1, 64)

MyMIDI_file = MIDIFile(1)
MyMIDI_file.addTempo(0, 0, TEMPO*2)

count = 0
while True:
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, TEMPO)

    lowest_note = 128
    highest_note = 0
    for i in range(256):
        note = ai_gen.__next__()
        if note >= LOWEST_NOTE and note <= HIGHEST_NOTE:
            #print(f"Note:{note}")
            if note < lowest_note:lowest_note=note
            if note > highest_note:highest_note=note
            MyMIDI.addNote(0, 0, note, i, DURATION, VOLUME)
            MyMIDI.addNote(0, 0, note + 4, i, DURATION, VOLUME)
            MyMIDI.addNote(0, 0, note + 7, i, DURATION, VOLUME)
            MyMIDI_file.addNote(0, 0, note, i + count, DURATION, VOLUME)
            MyMIDI_file.addNote(0, 0, note + 4, i + count, DURATION, VOLUME)
            MyMIDI_file.addNote(0, 0, note + 7, i + count, DURATION, VOLUME)
            count += 1
    #print(f"loweest note:{lowest_note}")
    #print(f"highest note:{highest_note}")

    with open("Generated.mid", "wb") as file:
        MyMIDI_file.writeFile(file)
    buf = io.BytesIO()
    MyMIDI.writeFile(buf)
    buf = io.BytesIO(buf.getbuffer())

    while mixer.music.get_busy():
        pass

    mixer.music.load(buf)
    mixer.music.play()


