import os
from google.cloud import speech

# Google Cloud APIキーの設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../private/google/notion-calendar-manager-bc1ebc32bf22.json"

def check_api_key():
    try:
        # Google Cloud Speech-to-Text APIのクライアントを初期化
        client = speech.SpeechClient()

        # ダミーの音声データを作成（無音データ）
        audio_data = speech.RecognitionAudio(content=b'\0' * 16000)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ja-JP"
        )

        # 音声認識リクエストを送信してレスポンスを確認
        response = client.recognize(config=config, audio=audio_data)
        print("APIキーが正しく設定されています。")
    except Exception as e:
        print(f"APIキーの確認中にエラーが発生しました: {e}")

if __name__ == "__main__":
    check_api_key()
