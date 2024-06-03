import openai
from openai import RateLimitError, Timeout, APIError, APIConnectionError, OpenAIError
import datetime

CHATGPT_API_KEY_PATH = "../../private/openai/chatGPT_api.txt"
FORMAT = """
        You are to understand my questions and respond in the following format:
        {
        "order": "",
        "contents": []
        }
        The key order should be chosen from schedule, reference, or other.
        schedule indicates scheduling an appointment in the calendar. In this case, contents should contain the appointment details in the format [month, day, time, title].
        reference is used to check the calendar schedule. In this case, contents should contain the schedule reference details in the format [month, day].
        other is used for any other input. In this case, contents should contain the input details in the format [text].
        Month, day, and time should be numerical values. Title and text should be strings.
        """

def read_keyFile():
    try:
        with open(CHATGPT_API_KEY_PATH, 'r', encoding='utf-8') as file:
            key = file.readline().strip()
        return key
    except FileNotFoundError:
        return "ファイルが見つかりません。"
    except Exception as e:
        return f"エラーが発生しました: {e}"

def main():
    openai.api_key = read_keyFile()

    question = input("質問内容：")
    dt_now = str(datetime.datetime.now())
    
    try:
        # 正しいAPIエンドポイントを使用してAPIキーの検証を行います
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "please speak japanese"},
                {"role": "system", "content": FORMAT},
                {"role": "system", "content": "[{}] now".format(dt_now)},
                {"role": "user", "content": question}
            ]
        )
        print("APIキーが正しく認識されています。")
        print(response.choices[0].message.content)
    except openai.AuthenticationError:
        print("APIキーが無効です。正しいAPIキーを設定してください。")
    except openai.RateLimitError:
        print("レートリミットに達しました。後でもう一度試してください。")
    except openai.OpenAIError as e:
        print(f"OpenAIのエラーが発生しました: {e}")



main()
