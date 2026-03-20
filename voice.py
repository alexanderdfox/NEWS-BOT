import subprocess
import uuid
import os
from pydub import AudioSegment

# -------- SETTINGS --------
questions = ["What?", "Who?", "Where?", "How?", "When?"]

voices = {
	"female": "Samantha",
	"male": "Alex",
	"child": "Fred"
}

offsets = {
	"female": 0,
	"male": 2,
	"child": 4
}

panning = {
	"female": -0.7,
	"male": 0.7,
	"child": 0.0
}

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# -------- GENERATE AUDIO FILE --------
def generate_voice(text, voice):
	filename = f"/tmp/{uuid.uuid4()}.aiff"
	subprocess.run(["say", "-v", voice, "-o", filename, text], check=True)
	return filename

# -------- BUILD MIX --------
def build_mix(text):
	tracks = []

	for role in voices:
		file = generate_voice(text, voices[role])
		sound = AudioSegment.from_file(file)

		# Apply offset
		sound = AudioSegment.silent(duration=offsets[role]) + sound

		# Apply stereo panning
		sound = sound.pan(panning[role])

		tracks.append(sound)

	# Mix tracks
	mix = tracks[0]
	for t in tracks[1:]:
		mix = mix.overlay(t)

	return mix

# -------- CLEAN FILENAME --------
def clean_name(text):
	return text.replace("?", "").lower()

# -------- MAIN LOOP --------
for q in questions:
	print(f"Processing: {q}")

	mix = build_mix(q)

	filename = os.path.join(output_dir, f"{clean_name(q)}.wav")

	# Export as WAV
	mix.export(filename, format="wav")

	print(f"Saved: {filename}")

print("Done.")