from music21 import converter, instrument, note, chord, stream
import glob

def extract_notes(midi_folder):
    notes = []
    for file in glob.glob(f"{midi_folder}/*.mid"):
        midi = converter.parse(file)
        parts = instrument.partitionByInstrument(midi)
        notes_to_parse = parts.parts[0].recurse() if parts else midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

def create_midi_from_notes(notes, output_file="generated_markov.mid"):
    output_notes = []
    for pattern in notes:
        if '.' in pattern:
            chord_notes = [note.Note(int(n)) for n in pattern.split('.')]
            new_chord = chord.Chord(chord_notes)
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            output_notes.append(new_note)
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=output_file)
