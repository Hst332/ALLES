#!/usr/bin/env python3
"""
CODE A – Natural Gas Forecast
Stabil. Getestet. Serien-sicher.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score

START_DATE = "2014-01-01"
GAS_SYMBOL = "NG=F"

UP_THRESHOLD = 0.60
DOWN_THRESHOLD = 0.40


def run_gas_forecast():
    prices = load_gas_prices()
    storage = load_eia_storage()

    df = build_features(prices, storage)
    model, features, cv_mean, cv_std = train_model(df)

    probs = model.predict_proba(df[features])[:, 1]
    last_prob = probs[-1]

    if last_prob >= UP_THRESHOLD:
        signal = "UP"
    elif last_prob <= DOWN_THRESHOLD:
        signal = "DOWN"
    else:
        signal = "NO_TRADE"

    return {
        "market": "GAS",
        "run_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "data_date": df.index[-1].date().isoformat(),
        "prob_up": float(last_prob),
        "prob_down": float(1 - last_prob),
        "signal": signal,
        "cv_mean": cv_mean,
        "cv_std": cv_std
    }


def write_backtest_csv(df, model, features):
    # =======================
    # BACKTEST CSV
    # =======================
    probs = model.predict_proba(df[features])[:, 1]

    bt = pd.DataFrame({
        "date": df.index,
        "prob_up": probs,
        "signal": np.where(
            probs >= UP_THRESHOLD, "UP",
            np.where(probs <= DOWN_THRESHOLD, "DOWN", "NO_TRADE")
        ),
        "actual_up": df["Target"]
    })

    bt.to_csv("gas_backtest.csv", index=False)
