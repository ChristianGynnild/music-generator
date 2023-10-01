import time
import mido
import os
import numpy as np
from tqdm import tqdm

DATA_PATH = "../Classical"
files = []

#Max difference is 84


for root_dir, folders, filenames in os.walk(DATA_PATH):
    for file in filenames:
        files.append(os.path.join(root_dir, file))


class Note():
    def __init__(self, time, note, duration):
        self.time = time
        self.note = note
        self.duration = duration

    def __repr__(self):
        return f"'Note' time:{round(self.time,2)}, note:{self.note}, duration:{self.duration}"


def midifile_to_notelist(midifile):
    notes = []
    time = 0
    active_notes_duration = [None] * 128
    active_notes = []

    for msg in midifile:
        time += msg.time

        for msg in active_notes:
            active_notes_duration[msg].duration += msg.time

        if msg.type == "note_on" or msg.type == "note_off":
            if msg.msg in active_notes:
                notes.append(active_notes_duration[msg.msg])
                active_notes.remove(msg.msg)

        if msg.type == "note_on" and msg.velocity != 0:
            active_notes_duration[msg.msg] = Note(time, msg.msg, 0)
            active_notes.append(msg.msg)

    notes = sorted(notes, key=lambda x: x.time)
    return notes


file = files[10]
print(file)
midifile = mido.MidiFile(file)
notes = midifile_to_notelist(midifile)

filtered_notes = []

current_notes = []
current_time = 0

for msg in notes:
    if current_time == msg.time:
        current_notes.append(msg)
    else:
        #print(current_time, ":", note)
        current_notes = sorted(current_notes, key=lambda x:x.msg)
        filtered_notes.append(current_notes[-1])
        current_notes = [msg]
        current_time = msg.time

current_notes = sorted(current_notes, key=lambda x:x.msg)
filtered_notes.append(current_notes[-1])

mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

track.append(mido.Message('program_change', program=56, time=0))
VELOCITY = 64
time = 0
TICKS_PER_BEAT = 10
TEMPO = 10

active_notes_duration = [0] * 128
active_notes = []


for i, msg in enumerate(notes):
    note_index = -1
    lowest_duration = msg.time-time
    for i, note_duration in enumerate(active_notes_duration):
        if lowest_duration > note_duration:
            lowest_duration = note_duration
            note_index = i


    if note_index != -1:
        relapse_time(-lowest_duration)
        track.append(mido.Message('note_on', note=msg.note, velocity=VELOCITY,time=mido.second2tick(delta_time, TICKS_PER_BEAT, TEMPO)))

    track.append(mido.Message('note_on', note=msg.note, velocity=VELOCITY, time=mido.second2tick(delta_time,TICKS_PER_BEAT,TEMPO)))
    time = msg.time
    active_notes_duration[msg.note] = msg.duration
    active_notes.append(msg.note)



#    msg.duration < notes[]

    track.append(mido.Message('note_off', note=msg.note, velocity=VELOCITY, time=128))

mid.save('mido_midi.mid')