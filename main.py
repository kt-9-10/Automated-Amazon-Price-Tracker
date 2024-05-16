import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib
import os

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

AMAZON_URL = "https://www.amazon.co.jp/%E6%B6%B2%E6%99%B6%E3%83%9A%E3%83%B3%E3%82%BF%E3%83%96%E3%83%AC%E3%83%83%E3%83%88-ACK05%E5%B7%A6%E6%89%8B%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9%E4%BB%98-%E3%82%B9%E3%82%BF%E3%83%B3%E3%83%89%E4%BB%98%E5%B1%9E-%E3%82%A4%E3%83%A9%E3%82%B9%E3%83%88%E5%88%B6%E4%BD%9C-%E3%81%8A%E7%B5%B5%E6%8F%8F%E3%81%8D%E3%80%8C2%E5%B9%B4%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC%E4%BF%9D%E8%A8%BC%E3%80%8D/dp/B0CJ98Y7F1/"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
}

# スクレイピングデータの取得
response = requests.get(AMAZON_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 価格の取得
price_str = soup.find(name="span", class_="a-price-whole").get_text()
price_int = int(price_str.replace(",", ""))

price_base = 59800
# 安値判定
if price_int <= price_base:

    # メッセージの作成
    content = f"現在の価格: {price_int}円\n製品を購入する: {AMAZON_URL}"
    subject = f"XPPen Artist Pro 14 の価格が{price_base}円以下になりました！"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = my_email

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)

