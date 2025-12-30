import os
print("[DEBUG] Working directory:", os.getcwd())

#!/usr/bin/env python3
"""
Backtest: Gas, WTI, Brent
Trefferquote bei verschiedenen Schwellen
"""

import numpy as np
import pandas as pd

from gas_forecast import (
    load_gas_prices,
    load_eia_storage,
    build_features,
    train_model
)

SYMBOLS = {
    "GAS": "NG=F",
    "WTI": "CL=F",
    "BRENT": "BZ=F"
}

THRESHOLDS = [0.53, 0.55, 0.57, 0.59, 0.61]


def run_backtest(symbol):
    import gas_forecast
    gas_forecast.GAS_SYMBOL = symbol

    prices = load_gas_prices()
    storage = load_eia_storage() if symbol == "NG=F" else None

    df = build_features(prices, storage)
    model, features, _, _ = train_model(df)

    probs = model.predict_proba(df[features])[:, 1]
    target = df["Target"].values

    rows = []

    for t in THRESHOLDS:
        signals = probs >= t
        trades = signals.sum()
        hits = ((signals) & (target == 1)).sum()

        hit_rate = hits / trades if trades > 0 else np.nan

        rows.append({
            "symbol": symbol,
            "threshold": t,
            "trades": int(trades),
            "hit_rate": round(hit_rate, 4) if trades > 0 else None
        })

    return rows


def main():
    all_rows = []

    for name, sym in SYMBOLS.items():
        print(f"[RUN] {name}")
        all_rows.extend(run_backtest(sym))

    df = pd.DataFrame(all_rows)
    df.to_csv("hit_rates_gas_wti_brent.csv", index=False)

    print("\n[OK] Backtest fertig → hit_rates_gas_wti_brent.csv\n")
    print(df)


if __name__ == "__main__":
    main()
