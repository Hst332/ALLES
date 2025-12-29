#!/usr/bin/env python3
"""
CODE A – Oil Forecast
Brent + WTI + Spread
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

START_DATE = "2015-01-01"
SYMBOL_BRENT = "BZ=F"
SYMBOL_WTI = "CL=F"

OUT_TXT = "forecast_oil.txt"

def load_prices():
    brent = yf.download(SYMBOL_BRENT, start=START_DATE, progress=False)
    wti = yf.download(SYMBOL_WTI, start=START_DATE, progress=False)

    df = pd.DataFrame(index=brent.index)
    df["Brent_Close"] = brent["Close"]
    df["WTI_Close"] = wti["Close"]
    return df.dropna()

def run_oil_forecast():
    df = load_prices()

    df["Brent_Trend"] = df["Brent_Close"] > df["Brent_Close"].rolling(20).mean()
    df["WTI_Trend"] = df["WTI_Close"] > df["WTI_Close"].rolling(20).mean()

    df["Spread"] = df["Brent_Close"] - df["WTI_Close"]
    df["Spread_Z"] = (
        (df["Spread"] - df["Spread"].rolling(60).mean())
        / df["Spread"].rolling(60).std()
    )

    df.dropna(inplace=True)
    last = df.iloc[-1]

    prob_up = 0.50
    if last["Brent_Trend"] and last["WTI_Trend"]:
        prob_up += 0.07
    if last["Spread_Z"] > 0.5:
        prob_up += 0.03
    elif last["Spread_Z"] < -0.5:
        prob_up -= 0.03

    prob_up = max(0, min(1, prob_up))
    prob_down = 1 - prob_up

    signal = "NO_TRADE"
    if prob_up >= 0.57:
        signal = "UP"
    elif prob_up <= 0.43:
        signal = "DOWN"

    with open(OUT_TXT, "w") as f:
        f.write("===================================\n")
        f.write("      OIL FORECAST – CODE A\n")
        f.write("===================================\n")
        f.write(f"Run time (UTC): {datetime.utcnow()}\n")
        f.write(f"Data date     : {last.name.date()}\n\n")
        f.write(f"Prob UP       : {prob_up:.2%}\n")
        f.write(f"Prob DOWN     : {prob_down:.2%}\n")
        f.write(f"Signal        : {signal}\n")
        f.write("===================================\n")
