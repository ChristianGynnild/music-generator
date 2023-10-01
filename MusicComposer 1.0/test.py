from pygame import mixer
import time
mixer.init()

filename = "/home/christian/PycharmProjects/MusicComposer/Generated.mid"
with open(filename, "rb") as file:
    mixer.music.load(file)
mixer.music.play()
time.sleep(1000)



# import time as t
# from pygame import mixer
# import midiutil
# import io
# from midiutil import MIDIFile
# import mido
#
# #https://youtu.be/2f20d0LJSuk
#
# file = "Classical/debussy/deb_menu.mid"
# notes = []
# for msg in mido.MidiFile(file):
#     if msg.type == "note_on":
#         notes.append(int(msg.note))
#
#
# duration = 1    # In beats
# tempo = 60*5   # In BPM
# volume = 100  # 0-127, as per the MIDI standard
#
# MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                       # automatically)
# MyMIDI.addTempo(0, 0, tempo)
#
# for i, pitch in enumerate(notes):
#     MyMIDI.addNote(0, 0, pitch, i, duration, volume)
# #endregion
#
# buf = io.BytesIO()
# MyMIDI.writeFile(buf)
# buf = io.BytesIO(buf.getbuffer())
#
# mixer.init()
#
# mixer.music.load(buf)
# mixer.music.play()
# t.sleep(100000)