import markovify
from music_utils import extract_notes, create_midi_from_notes

# Load notes from MIDI files
notes = extract_notes("midi")
print(f"✅ Loaded {len(notes)} notes from MIDI files.")

# Build Markov model
text = ' '.join(notes)
model = markovify.NewlineText(text)

# Generate new notes
generated_notes = []
for _ in range(100):
    next_note = model.make_sentence()
    if next_note:
        generated_notes.extend(next_note.split())

# Save to MIDI
create_midi_from_notes(generated_notes)
print("🎵 Music generated and saved to generated_markov.mid")
