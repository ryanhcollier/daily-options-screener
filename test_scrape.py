import requests
from bs4 import BeautifulSoup

ticker = "AAPL"
url = f"https://www.alphaquery.com/stock/{ticker}/volatility-option-statistics/30-day/iv-mean"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

res = requests.get(url, headers=headers)
with open("aapl_aq.html", "w") as f:
    f.write(res.text)

