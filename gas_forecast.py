from datetime import datetime
import json
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score

START_DATE = "2014-01-01"
GAS_SYMBOL = "NG=F"
UP_THRESHOLD = 0.60
DOWN_THRESHOLD = 0.40

def run_gas_forecast():
    df = yf.download(GAS_SYMBOL, start=START_DATE, auto_adjust=True, progress=False)
    df = df[["Close"]].rename(columns={"Close": "Gas_Close"}).dropna()

    df["ret"] = df["Gas_Close"].pct_change()
    df["trend_5"] = df["Gas_Close"].pct_change(5)
    df["trend_20"] = df["Gas_Close"].pct_change(20)
    df["vol_10"] = df["ret"].rolling(10).std()
    df["Target"] = (df["ret"].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)

    X = df[["trend_5", "trend_20", "vol_10"]]
    y = df["Target"]

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    prob_up = model.predict_proba(X.iloc[-1:])[0][1]

    signal = (
        "UP" if prob_up >= UP_THRESHOLD else
        "DOWN" if prob_up <= DOWN_THRESHOLD else
        "NO_TRADE"
    )

    return f"""===================================
   NATURAL GAS FORECAST – CODE A
===================================
Run time (UTC): {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}
Data date     : {df.index[-1].date()}

Prob UP       : {prob_up:.2%}
Prob DOWN     : {1-prob_up:.2%}
Signal        : {signal}
===================================
"""
