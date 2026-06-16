import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

STOCK = "NVDA"

def fetch_ticker(name):
    ticker = yf.Ticker(name)
    return ticker

def get_metrics(ticker):
    info = ticker.info

    # value metrics
    metrics = {
        "pe_ratio": info.get("trailingPE"),   # P/E ratio
        "pb_ratio": info.get("priceToBook"),  # P/B ratio
        "dividen_yield": info.get("dividendYield"),
    }

    # quality metrics
    metrics.update({
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAsset"),
        "debt_to_equity": info.get("deptToEquity")
    })

    # volatility metrics
    metrics.update({
        "beta": info.get("beta")
    })

    return metrics

def get_hist_factors(ticker, period="1y"):
    history = ticker.history(period=period)
          
    factors = dict()
    # Momentum & volatility (require historical data)
    daily_returns = history["Close"].pct_change().dropna()
    factors["volatility"] = daily_returns.std()

    # 6-month momentum
    if len(history) >= 126:
        # iloc[-2] since the last one (current) is always nan
        factors["momentum_6m"] = history["Close"].iloc[-2] / history["Close"].iloc[-126] - 1

    # 12-month momentum
    if len(history) >= 252:
        factors["momentum_12m"] = history["Close"].iloc[-2] / history["Close"].iloc[-252] - 1

    # momentum of defined period
    factors["momentum_period"] = history["Close"].iloc[-2] / history["Close"].iloc[0] - 1
    return factors


ticker = fetch_ticker(STOCK)
print(get_metrics(ticker))
print(get_hist_factors(ticker))




