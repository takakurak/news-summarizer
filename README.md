# Automated News Summary & Notification Bot 🤖

## Overview

This repository contains a Python script that automatically collects the latest news articles related to specified keywords, summarizes and translates them using AI (OpenAI, Gemini, DeepSeek), and notifies a designated Slack or Discord channel. It is designed to be run periodically using GitHub Actions.

## ✨ Key Features

  * **News Collection**: Fetches the latest news articles containing keywords of interest using the NewsAPI.
  * **AI-Powered Summarization & Translation**: Utilizes AI models from OpenAI (GPT), Google (Gemini), or DeepSeek to summarize and translate article content into a specified language (defaults to Japanese).
  * **Notification Functionality**: Sends the generated summaries to a Slack or Discord webhook URL.
  * **Automated Execution**: Runs automatically at a scheduled time every day (default: 9:00 AM UTC) via GitHub Actions. Manual execution is also possible.
  * **Flexible Customization**: Easily customize search keywords, notification destinations, and the AI model to be used by changing environment variables (GitHub Secrets).

## 🚀 Setup Instructions

### 1\. Fork the Repository

First, fork this repository to your own GitHub account.

### 2\. Obtain API Keys from External Services

To run this script, you will need the following API keys and URLs:

  * **NewsAPI**: Required to fetch news articles. Sign up on the [official NewsAPI website](https://newsapi.org/) to get your API key.
  * **AI Model API Key**: Used for summarizing articles. Obtain at least one of the following:
      * [OpenAI API Key](https://platform.openai.com/signup/)
      * [Google AI (Gemini) API Key](https://ai.google.dev/pricing)
      * [DeepSeek API Key](https://platform.deepseek.com/)
      * **Note**: The script will automatically select an available key in the following order of priority: `DeepSeek` \> `OpenAI` \> `Gemini`.
  * **Notification Webhook URL**: Required to send the summary results.
      * [Slack Incoming Webhook URL](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)
      * [Discord Webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

### 3\. Configure GitHub Repository Secrets

In your forked repository, navigate to `Settings` \> `Secrets and variables` \> `Actions`. Click `New repository secret` to add the following information. For the `Value`, enter the keys and URLs you obtained in Step 2.

#### Required Secrets

| Secret Name | Description |
| :--- | :--- |
| `NEWS_API_KEY` | Your API key for NewsAPI. |
| At least one AI API key | One of `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, or `GEMINI_API_KEY`. |
| At least one Webhook URL | Either `SLACK_WEBHOOK_URL` or `DISCORD_WEBHOOK_URL`. |

#### Optional Secrets (Configure as needed)

| Secret Name | Description | Default Value |
| :--- | :--- | :--- |
| `SEARCH_KEYWORDS` | Keywords to search for with NewsAPI. | `(insect OR animal) AND (research OR study)` |
| `SELECT_TOP_N` | The number of articles to actually summarize after sorting by relevancy score. | `5` |
| `MAX_ARTICLES` | The maximum number of articles to fetch from NewsAPI at once. | `20` |
| `OPENAI_MODEL` | The name of the OpenAI model to use. | `gpt-3.5-turbo` |
| `GEMINI_MODEL` | The name of the Gemini model to use. | `gemini-1.0-pro` |
| `TARGET_LANGUAGE` | The target language for translation and summarization. | `ja` (Japanese) |

### 4\. Enable GitHub Actions

Go to the `Actions` tab of your forked repository and click `I understand my workflows, go ahead and enable them` to enable the workflow.

Setup is now complete\! The workflow will run automatically at the scheduled time (default: every day at 9:00 AM UTC).

### ✋ Manual Execution

If you want to test the script immediately, you can also run it manually from `Actions` \> `Daily News Summary` \> `Run workflow`.

## 📂 File Structure

```
.
├── .github/workflows/
│   └── news_summary.yml   # GitHub Actions workflow definition file
├── main.py                # Main Python script
└── requirements.txt       # Python dependency list
```

## ⚠️ Disclaimer

  * This script uses external APIs. Please review the terms of service and pricing for each service and use at your own risk.
  * The cron schedule in `news_summary.yml` (`0 9 * * *`) is in UTC. Please adjust it if you need to run it at a different time.
