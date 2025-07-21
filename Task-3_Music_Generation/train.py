import numpy as np
from music21 import instrument, note, stream
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
from keras.utils import to_categorical
from midi_utils import get_notes_from_midi
import pickle, os

notes = get_notes_from_midi('midi')

seq_len = 100
pitches = sorted(set(notes))
note_to_int = dict((note, num) for num, note in enumerate(pitches))

network_input = []
network_output = []

for i in range(0, len(notes) - seq_len):
    seq_in = notes[i:i + seq_len]
    seq_out = notes[i + seq_len]
    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)
network_input = np.reshape(network_input, (n_patterns, seq_len, 1)) / float(len(pitches))
network_output = to_categorical(network_output)

model = Sequential()
model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(len(pitches)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(network_input, network_output, epochs=20, batch_size=64)

model.save('music_model.h5')
with open('mapping.pkl', 'wb') as f:
    pickle.dump((note_to_int, pitches), f)
