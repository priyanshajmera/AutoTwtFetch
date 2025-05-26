# Tweet Watcher 📡

Monitors a Twitter account using `snscrape` and sends full tweets to your email when a new one is posted.

## Features

- Monitors a specified Twitter user (no API key needed)
- Sends email with full tweet content + link
- Runs 24×7 as a background worker on Render

## Setup on Render

1. Create a new GitHub repo with this code
2. Go to [https://render.com](https://render.com)
3. Click **"New +" → "Background Worker"**
4. Connect your GitHub repo
5. Set environment variables:
   - `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`
   - `TWITTER_HANDLE` (optional, defaults to `elonmusk`)
6. Deploy and let it run forever 🚀

## Example Email Output

