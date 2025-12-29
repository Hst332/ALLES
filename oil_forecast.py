from datetime import datetime
import pandas as pd
import yfinance as yf

START_DATE = "2015-01-01"
SYMBOL_BRENT = "BZ=F"
SYMBOL_WTI = "CL=F"

def run_oil_forecast():
    brent = yf.download(SYMBOL_BRENT, start=START_DATE, progress=False)
    wti = yf.download(SYMBOL_WTI, start=START_DATE, progress=False)

    df = pd.DataFrame(index=brent.index)
    df["Brent"] = brent["Close"]
    df["WTI"] = wti["Close"]
    df.dropna(inplace=True)

    df["Spread"] = df["Brent"] - df["WTI"]
    df["Trend"] = (df["Brent"] > df["Brent"].rolling(20).mean()) & \
                  (df["WTI"] > df["WTI"].rolling(20).mean())

    last = df.iloc[-1]
    prob_up = 0.57 if last["Trend"] else 0.47

    signal = (
        "UP" if prob_up >= 0.57 else
        "DOWN" if prob_up <= 0.43 else
        "NO_TRADE"
    )

    return f"""===================================
      OIL FORECAST – CODE A
===================================
Run time (UTC): {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}
Data date     : {df.index[-1].date()}

Brent Close   : {last['Brent']:.2f}
WTI Close     : {last['WTI']:.2f}
Brent–WTI Spd : {last['Spread']:.2f}

Prob UP       : {prob_up:.2%}
Prob DOWN     : {1-prob_up:.2%}
Signal        : {signal}
===================================
"""
