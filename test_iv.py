import requests

ticker = "AAPL"
url = f"https://www.alphaquery.com/data/option-statistic-chart?ticker={ticker}&perType=30-Day&identifier=iv-mean"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    res = requests.get(url, headers=headers)
    data = res.json()
    print("Number of records:", len(data))
    if len(data) > 0:
        values = [d['value'] for d in data if d.get('value') is not None]
        if values:
            min_iv = min(values)
            max_iv = max(values)
            current_iv = values[-1]
            if max_iv > min_iv:
                iv_rank = (current_iv - min_iv) / (max_iv - min_iv) * 100
            else:
                iv_rank = 50.0
            print(f"Calculated IV Rank: {iv_rank:.2f}%")
except Exception as e:
    print(e)
