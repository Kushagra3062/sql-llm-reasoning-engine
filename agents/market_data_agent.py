import yfinance as yf
from schema import State

def market_data_agent(state: State):
    print("\n[MARKET_DATA] Fetching live market metrics...")
    
    context = state.get("structured_context", {})
    query = state.get("resolved_query", "")
    
    # Try to find a ticker. Assume memory agent placed it in resolved_query or structured context.
    # Fallback heuristic: check if common tickers are in the query
    possible_tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "TSLA", "META"]
    target_ticker = None
    
    for t in possible_tickers:
        if t in query.upper() or list(context.values()).count(t) > 0:
            target_ticker = t
            break
            
    if not target_ticker:
        return {"market_data": "Could not identify a valid stock ticker for this request."}
        
    try:
        stock = yf.Ticker(target_ticker)
        
        # Fetch last 5 days history
        hist = stock.history(period="5d")
        if hist.empty:
            data = f"No recent market data found for {target_ticker}."
        else:
            latest = hist.iloc[-1]
            price = latest['Close']
            volume = latest['Volume']
            trend = "Up" if hist.iloc[-1]['Close'] > hist.iloc[0]['Close'] else "Down"
            
            data = {
                "Ticker": target_ticker,
                "Current Price": f"${price:.2f}",
                "Volume": int(volume),
                "5-Day Trend": trend
            }
            
        return {"market_data": data}
        
    except Exception as e:
        print(f"[MARKET_DATA] Error fetching info: {e}")
        return {"market_data": f"Failed to retrieve market data for {target_ticker}."}
