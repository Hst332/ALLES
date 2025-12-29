# main.py
from gas_forecast import run_gas_forecast
from oil_forecast import run_oil_forecast

OUTPUT_FILE = "forecast_combined.txt"

def main():
    gas = run_gas_forecast()
    oil = run_oil_forecast()

    text = f"""
===================================
        ENERGY FORECAST – CODE A
===================================

--- NATURAL GAS ---
Run time (UTC): {gas['run_time']}
Data date     : {gas['data_date']}
Gas Price     : {gas['price']:.2f}
Prob UP       : {gas['prob_up']:.2%}
Prob DOWN     : {gas['prob_down']:.2%}
Signal        : {gas['signal']}

--- CRUDE OIL ---
Run time (UTC): {oil['run_time']}
Data date     : {oil['data_date']}
Brent         : {oil['brent']:.2f}
WTI           : {oil['wti']:.2f}
Spread        : {oil['spread']:.2f}
Prob UP       : {oil['prob_up']:.2%}
Prob DOWN     : {oil['prob_down']:.2%}
Signal        : {oil['signal']}

===================================
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text.strip())

    print("[OK] forecast_combined.txt written")

if __name__ == "__main__":
    main()
