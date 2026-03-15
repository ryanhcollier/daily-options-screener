from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/ivrank/{ticker}")
async def get_iv_rank(ticker: str):
    ticker = ticker.upper()
    url = f"https://www.alphaquery.com/data/option-statistic-chart?ticker={ticker}&perType=30-Day&identifier=iv-mean"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail="No historical IV data returned for this ticker")
            
        values = [d['value'] for d in data if d.get('value') is not None]
        if not values:
            raise HTTPException(status_code=404, detail="No valid IV values found in data")
            
        min_iv = min(values)
        max_iv = max(values)
        current_iv = values[-1]
        
        if max_iv > min_iv:
            # Traditional IV Rank formula: (Current IV - 52W Low IV) / (52W High IV - 52W Low IV)
            # AlphaQuery gives roughly 3 months of data here, providing a 90-Day IV Rank.
            iv_rank = (current_iv - min_iv) / (max_iv - min_iv) * 100
        else:
            iv_rank = 50.0
            
        return {"ticker": ticker, "ivRank": round(iv_rank, 2)}
        
    except requests.RequestException as e:
        print(f"Request Error fetching IV data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Target site request failed: {e}")
    except Exception as e:
        print(f"Unknown Error calculating IV Rank for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Internal parsing error")

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
