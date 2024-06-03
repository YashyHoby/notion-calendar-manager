from pynput import keyboard
import os
import pyaudio
from google.cloud import speech

# Google Cloud APIキーの設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../private/google/notion-calendar-manager-bc1ebc32bf22.json"

# キーの状態を追跡するための変数
r_pressed = False
recording = False

def on_press(key):
    global r_pressed, recording
    if key == keyboard.Key.esc:
        # プログラムを終了するためのキー
        return False
    try:
        if key.char == 'r' and not r_pressed:
            print('rキーが押されました')
            r_pressed = True
            recording = True
            # 録音を開始する
            record_audio()
    except AttributeError:
        pass

def on_release(key):
    global r_pressed, recording
    try:
        if key.char == 'r' and r_pressed:
            print('rキーが離されました')
            r_pressed = False
            recording = False
            # 録音を停止する
            stop_recording()
    except AttributeError:
        pass

client = speech.SpeechClient()

# 音声録音の設定
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
audio = pyaudio.PyAudio()
stream = None

def record_audio():
    global stream, recording
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

def stop_recording():
    global stream, recording
    print("Recording finished.")
    frames = []
    while recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    transcribe_speech(b''.join(frames))
    
def transcribe_speech(audio_data):
    # audio_dataが空でないことを確認
    if not audio_data:
        print('録音された音声データがありません。')
        return

    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='ja-JP'
    )

    try:
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
    except google.api_core.exceptions.GoogleAPIError as e:
        print('Google Speech-to-Text APIからエラーが返されました:', e)

# リスナーの登録
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()
