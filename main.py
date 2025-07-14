import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

def fetch_news():
    """NewsAPIから最新のニュースを取得"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "AI",  # 検索キーワード（例: AI）
        "from": "2024-02-10",  # 24時間以内の記事を取得
        "sortBy": "publishedAt",
        "apiKey": os.getenv("NEWS_API_KEY"),
        "pageSize": 5  # 最大5記事
    }
    response = requests.get(url, params=params)
    return response.json().get("articles", [])

def summarize_with_gpt(text):
    """OpenAIで要約を生成"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"以下のニュース記事を簡潔に要約し、背景を説明してください:\n\n{text}"
        }]
    )
    return response.choices[0].message.content

def send_to_slack(message):
    """Slackに通知"""
    payload = {"text": message}
    requests.post(os.getenv("SLACK_WEBHOOK_URL"), json=payload)

def main():
    articles = fetch_news()
    for article in articles:
        summary = summarize_with_gpt(f"{article['title']}\n\n{article['description']}")
        send_to_slack(f"*{article['title']}*\n{summary}\n\nリンク: {article['url']}")

if __name__ == "__main__":
    main()
