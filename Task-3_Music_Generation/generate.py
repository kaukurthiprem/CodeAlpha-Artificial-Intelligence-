import numpy as np
from keras.models import load_model
from music21 import instrument, note, stream, chord
import pickle
from midi_utils import get_notes_from_midi

with open('mapping.pkl', 'rb') as f:
    note_to_int, pitches = pickle.load(f)
int_to_note = dict((num, note) for note, num in note_to_int.items())

model = load_model('music_model.h5')

sequence = get_notes_from_midi('midi')[:100]
pattern = [note_to_int[n] for n in sequence]
prediction_output = []

for _ in range(100):
    input_seq = np.reshape(pattern, (1, len(pattern), 1)) / float(len(pitches))
    prediction = model.predict(input_seq, verbose=0)
    idx = np.argmax(prediction)
    result = int_to_note[idx]
    prediction_output.append(result)
    pattern.append(idx)
    pattern = pattern[1:]

output_notes = []
for item in prediction_output:
    if '.' in item:
        chord_notes = [note.Note(int(n)) for n in item.split('.')]
        new_chord = chord.Chord(chord_notes)
        output_notes.append(new_chord)
    else:
        new_note = note.Note(item)
        output_notes.append(new_note)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='output/generated.mid')
print("🎵 Music generated and saved to output/generated.mid")
