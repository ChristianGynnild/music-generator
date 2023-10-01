import pickle
from midiutil import MIDIFile
import io
from pygame import mixer, time
import pygame
import random

with open("data.cache", "rb") as file:
    data = pickle.load(file)

random.shuffle(data)

DURATION = 1    # In beats
TEMPO = 60 * 8   # In BPM
VOLUME = 100  # 0-127, as per the MIDI standard

pygame.mixer.init(44100, -16, 1, 64)


for batch in data:
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(0, 0, TEMPO)

    for i, pitch in enumerate(batch):
        MyMIDI.addNote(0, 0, pitch, i, DURATION, VOLUME)

    buf = io.BytesIO()
    MyMIDI.writeFile(buf)
    buf = io.BytesIO(buf.getbuffer())

    while mixer.music.get_busy():
        pass

    mixer.music.load(buf)
    mixer.music.play()

