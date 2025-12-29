# gas_forecast.py
import yfinance as yf
import pandas as pd
from datetime import datetime

START_DATE = "2014-01-01"
GAS_SYMBOL = "NG=F"

def run_gas_forecast():
    df = yf.download(GAS_SYMBOL, start=START_DATE, auto_adjust=True, progress=False)
    df = df[["Close"]].rename(columns={"Close": "Gas_Close"}).dropna()

    df["trend_20"] = df["Gas_Close"] > df["Gas_Close"].rolling(20).mean()
    df["ret"] = df["Gas_Close"].pct_change()
    df = df.dropna()

    last = df.iloc[-1]

    prob_up = 0.50
    if last["trend_20"]:
        prob_up += 0.10

    prob_up = min(max(prob_up, 0.0), 1.0)

    if prob_up >= 0.60:
        signal = "UP"
    elif prob_up <= 0.40:
        signal = "DOWN"
    else:
        signal = "NO_TRADE"

    return {
        "run_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "data_date": last.name.date().isoformat(),
        "prob_up": prob_up,
        "prob_down": 1 - prob_up,
        "signal": signal,
        "price": float(last["Gas_Close"]),
    }
