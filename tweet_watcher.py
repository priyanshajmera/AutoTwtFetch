import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import snscrape.modules.twitter as sntwitter
import os
import ssl
import certifi

# SSL fix for cert verification on Render
os.environ['SSL_CERT_FILE'] = certifi.where()

TWITTER_HANDLE = os.getenv("TWITTER_HANDLE", "elonmusk")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]

LAST_TWEET_ID = None

def send_email_notification(tweet_id, tweet_content):
    tweet_url = f"https://twitter.com/{TWITTER_HANDLE}/status/{tweet_id}"
    subject = f"New Tweet from @{TWITTER_HANDLE}"

    text_body = f"""New tweet from @{TWITTER_HANDLE}:\n\n{tweet_content}\n\nLink: {tweet_url}"""
    html_body = f"""<html><body><h3>New Tweet from @{TWITTER_HANDLE}</h3><p>{tweet_content}</p><p><a href="{tweet_url}">View Tweet</a></p></body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Email error: {e}")

def get_latest_tweet():
    try:
        scraper = sntwitter.TwitterUserScraper(TWITTER_HANDLE)
        tweet = next(scraper.get_items())
        return tweet.id, tweet.content
    except Exception as e:
        print(f"❌ Scrape error: {e}")
        return None, None

if __name__ == "__main__":
    print(f"🔍 Monitoring @{TWITTER_HANDLE} for new tweets...")
    while True:
        tweet_id, content = get_latest_tweet()
        if tweet_id and tweet_id != LAST_TWEET_ID:
            print(f"\n🆕 New tweet:\n{content}")
            send_email_notification(tweet_id, content)
            LAST_TWEET_ID = tweet_id
        time.sleep(CHECK_INTERVAL)
