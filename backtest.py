import pandas as pd
from datetime import datetime

def write_backtest_csv(df, prob_col, signal_col, filename):
    out = pd.DataFrame({
        "date": df.index,
        "prob_up": df[prob_col],
        "signal": df[signal_col],
    })

    out.to_csv(filename, index=False)
    print(f"[OK] {filename} written")
