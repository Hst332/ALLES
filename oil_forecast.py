import yfinance as yf
import pandas as pd
from datetime import datetime

START_DATE = "2015-01-01"
SYMBOL_BRENT = "BZ=F"
SYMBOL_WTI = "CL=F"

def run_oil_forecast():
    brent = yf.download(SYMBOL_BRENT, start=START_DATE, progress=False)
    wti = yf.download(SYMBOL_WTI, start=START_DATE, progress=False)

    if brent.empty or wti.empty:
        raise RuntimeError("Oil data download failed")

    df = pd.DataFrame(index=brent.index)
    df["Brent"] = brent["Close"]
    df["WTI"] = wti["Close"]
    df.dropna(inplace=True)

    df["Brent_Trend"] = df["Brent"] > df["Brent"].rolling(20).mean()
    df["WTI_Trend"] = df["WTI"] > df["WTI"].rolling(20).mean()

    df["Spread"] = df["Brent"] - df["WTI"]
    df["Spread_Z"] = (
        (df["Spread"] - df["Spread"].rolling(60).mean())
        / df["Spread"].rolling(60).std()
    )

    df.dropna(inplace=True)
    last = df.iloc[-1]

    prob_up = 0.50
    if last["Brent_Trend"] and last["WT
