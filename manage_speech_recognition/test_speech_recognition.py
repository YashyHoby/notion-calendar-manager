import os
import time
import pyaudio
from google.cloud import speech

# Google Cloud APIキーの設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../private/google/notion-calendar-manager-bc1ebc32bf22.json"

client = speech.SpeechClient()

# 音声録音の設定
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def record_audio(duration):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)

def transcribe_speech(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='ja-JP'
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

def main():
    duration = 5  # 5秒間録音
    audio_data = record_audio(duration)
    transcribe_speech(audio_data)

main()
