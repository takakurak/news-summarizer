# ニュース自動要約＆通知ボット 🤖

## 概要

このリポジトリは、指定したキーワードに関連する最新のニュース記事を自動的に収集し、AI（OpenAI, Gemini, DeepSeek）を利用して要約・翻訳し、指定されたSlackまたはDiscordチャンネルに通知するPythonスクリプトです。GitHub Actionsを利用して、毎日定時に自動実行するように設計されています。

## ✨ 主な機能

  * **ニュース収集**: NewsAPIを利用して、関心のあるキーワードを含む最新のニュース記事を取得します。
  * **AIによる要約・翻訳**: OpenAI(GPT), Google(Gemini), DeepSeekのいずれかのAIモデルを使用して、記事の内容を指定した言語（デフォルトは日本語）に要約・翻訳します。
  * **通知機能**: 生成された要約をSlackまたはDiscordのWebhook URLに送信します。
  * **自動実行**: GitHub Actionsにより、毎日定刻（デフォルトは日本時間18:00）に自動で実行されます。手動での実行も可能です。
  * **柔軟なカスタマイズ**: 環境変数（GitHub Secrets）を変更することで、検索キーワード、通知先、使用するAIモデルなどを簡単にカスタマイズできます。

## 🚀 セットアップ手順

### 1\. リポジトリをフォークする

まず、このリポジトリをあなた自身のGitHubアカウントにフォークしてください。

### 2\. 外部サービスのAPIキーを取得する

このスクリプトを実行するには、以下のAPIキーなどが必要です。

  * **NewsAPI**: ニュース記事を取得するために必要です。[NewsAPIの公式サイト](https://newsapi.org/)でサインアップし、APIキーを取得してください。
  * **AIモデルのAPIキー**: 記事の要約に使用します。以下のいずれか1つ以上を取得してください。
      * [OpenAI API Key](https://platform.openai.com/signup/)
      * [Google AI (Gemini) API Key](https://ai.google.dev/pricing)
      * [DeepSeek API Key](https://platform.deepseek.com/)
      * **注**: スクリプトは `DeepSeek` \> `OpenAI` \> `Gemini` の優先順位で利用可能なキーを自動的に選択します。
  * **通知先のWebhook URL**: 要約結果を通知するために必要です。
      * [Slack Incoming Webhook URL](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)
      * [Discord Webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

### 3\. GitHubリポジトリにSecretsを設定する

フォークしたリポジトリの `Settings` \> `Secrets and variables` \> `Actions` に移動し、`New repository secret` をクリックして、以下の情報を登録します。`Value`には、ステップ2で取得したキーなどを入力してください。

#### 必須のSecret

| Secret名 | 説明 |
| :--- | :--- |
| `NEWS_API_KEY` | NewsAPIのAPIキー。 |
| いずれかのAI APIキー | `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` のうち最低1つ。 |
| いずれかのWebhook URL | `SLACK_WEBHOOK_URL` または `DISCORD_WEBHOOK_URL` のどちらか1つ。 |

#### オプションのSecret（任意で設定）

| Secret名 | 説明 | デフォルト値 |
| :--- | :--- | :--- |
| `SEARCH_KEYWORDS` | NewsAPIで検索するキーワード。 | `(insect OR animal) AND (research OR study)` |
| `SELECT_TOP_N` | 関連度スコアでソートした後、実際に要約する記事の数。 | `5` |
| `MAX_ARTICLES` | NewsAPIから一度に取得する最大記事数。 | `20` |
| `OPENAI_MODEL` | 使用するOpenAIのモデル名。 | `gpt-3.5-turbo` |
| `GEMINI_MODEL` | 使用するGeminiのモデル名。 | `gemini-1.0-pro` |
| `TARGET_LANGUAGE` | 翻訳・要約するターゲット言語。 | `ja` (日本語) |

### 4\. GitHub Actionsを有効化する

フォークしたリポジトリの `Actions` タブに移動し、`I understand my workflows, go ahead and enable them` をクリックしてワークフローを有効化してください。

これでセットアップは完了です！スケジュールされた時間（デフォルトは毎日日本時間18時）にワークフローが自動実行されます。

### ✋ 手動実行

すぐに動作確認をしたい場合は、`Actions` \> `Daily News Summary` \> `Run workflow`から手動で実行することもできます。

## 📂 ファイル構成

```
.
├── .github/workflows/
│   └── news_summary.yml   # GitHub Actions ワークフロー定義ファイル
├── main.py                # メインのPythonスクリプト
└── requirements.txt       # Pythonの依存ライブラリ
```

## ⚠️ 注意事項

  * このスクリプトは外部のAPIを利用しています。各サービスの利用規約や料金体系をご確認の上、ご自身の責任でご利用ください。
  * `news_summary.yml` 内のcronスケジュール (`0 9 * * *`) はUTC基準です。日本時間では18時になります。必要に応じて変更してください。
