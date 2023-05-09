import vosk
import pyaudio
import json

model = vosk.Model("vosk-model-small-ru-0.22")
print('------')


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            command = json.loads(rec.Result())
            if command['text']:
                yield command['text']


rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=16000
)
stream.start_stream()


for text in listen():
    print(text)