import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 環境変数の読み込み
load_dotenv()

def fetch_recent_news():
    """NewsAPIから24時間以内の関連ニュースを取得"""
    url = "https://newsapi.org/v2/everything"
    
    # キーワード設定（OR条件で複数指定、AND条件も可能）
    keywords = "(AI OR 人工知能 OR 機械学習 OR deep learning) AND (開発 OR 技術 OR 研究)"
    
    # 24時間前の日時を計算
    date_24h_ago = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
    
    params = {
        "q": keywords,
        "from": date_24h_ago,
        "sortBy": "relevancy",  # 関連度順でソート
        "language": "ja",       # 日本語記事に限定（必要に応じて調整）
        "apiKey": os.getenv("NEWS_API_KEY"),
        "pageSize": 5,          # 上位5記事
        "excludeDomains": "example.com,spam.site"  # 除外したいドメイン
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"NewsAPIリクエストエラー: {e}")
        return []

def summarize_with_gpt(text):
    """OpenAIで要約を生成（コスト最適化版）"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",  # 最新の効率的なモデル
            messages=[{
                "role": "user",
                "content": f"以下のニュースを日本語で簡潔に要約し、技術的な重要性を1文で説明してください（150字以内）:\n\n{text}"
            }],
            temperature=0.3,  # 創造性を低くし事実ベースに
            max_tokens=150    # 出力トークン制限
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI処理エラー: {e}")
        return "要約の生成に失敗しました"

def send_to_slack(message):
    """Slackに通知（リッチフォーマット版）"""
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            os.getenv("SLACK_WEBHOOK_URL"),
            json=payload,
            timeout=5
        )
        if response.status_code != 200:
            print(f"Slack送信エラー: {response.text}")
    except Exception as e:
        print(f"Slack接続エラー: {e}")

def main():
    print("=== ニュース収集開始 ===")
    
    articles = fetch_recent_news()
    if not articles:
        send_to_slack(":warning: 本日の関連ニュースは見つかりませんでした")
        return

    for article in articles:
        # 記事内容の前処理（長すぎる場合は切り詰め）
        content = f"{article['title']}\n\n{article.get('description', '')}"
        content = content[:2000]  # トークン節約のため制限
        
        summary = summarize_with_gpt(content)
        
        # Slackメッセージの整形
        message = (
            f":newspaper: *【{article['source']['name']}】{article['title']}*\n"
            f"*要約*: {summary}\n"
            f"*公開日時*: {article['publishedAt']}\n"
            f"<{article['url']}|記事を読む>"
        )
        
        send_to_slack(message)
        print(f"処理済み: {article['title']}")
    
    print("=== 処理完了 ===")

if __name__ == "__main__":
    main()
