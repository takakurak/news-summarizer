import os
import requests
from openai import OpenAI
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 検索キーワード (英語)
SEARCH_QUERY = "(insect OR animal OR behavior OR ecology) AND (paper OR discovery OR research)"

def fetch_english_news():
    """英語のニュースを取得"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": SEARCH_QUERY,
        "from": (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d"),
        "sortBy": "publishedAt",
        "language": "en",  # 英語記事のみ
        "apiKey": os.getenv("NEWS_API_KEY"),
        "pageSize": 5  # 最大5記事
    }
    response = requests.get(url, params=params)
    return response.json().get("articles", [])

def translate_and_summarize(text):
    """英語を日本語に翻訳・要約"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 翻訳と要約を同時にリクエスト
    prompt = f"""以下の英語テキストを日本語に翻訳し、簡潔に要約してください:

{text}

翻訳と要約:
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # 創造性を抑える
    )
    return response.choices[0].message.content

def send_to_slack(message):
    """Slackに通知"""
    payload = {"text": message}
    requests.post(os.getenv("SLACK_WEBHOOK_URL"), json=payload)

def main():
    articles = fetch_english_news()
    for article in articles:
        # タイトルと本文を結合して処理
        content = f"Title: {article['title']}\n\nContent: {article['description'] or 'No description available'}"
        japanese_summary = translate_and_summarize(content)
        
        # 通知メッセージ作成
        message = (
            f"*【英語記事の日本語要約】*\n"
            f"{japanese_summary}\n\n"
            f"*元記事リンク*: {article['url']}\n"
            f"*公開日時*: {article['publishedAt']}"
        )
        send_to_slack(message)

if __name__ == "__main__":
    main()
    
