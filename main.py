from gas_forecast import run_gas_forecast
from oil_forecast import run_oil_forecast

OUT_TXT = "combined_forecast.txt"


def main():
    gas = run_gas_forecast()
    oil = run_oil_forecast()

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("===================================\n")
        f.write("      ENERGY FORECAST – CODE A\n")
        f.write("===================================\n\n")

        for res in (gas, oil):
            f.write(f"{res['asset']}\n")
            f.write(f"Run time (UTC): {res['run_time']}\n")
            f.write(f"Data date     : {res['data_date']}\n")
            f.write(f"Prob UP       : {res['prob_up']:.2%}\n")
            f.write(f"Prob DOWN     : {res['prob_down']:.2%}\n")
            f.write(f"Signal        : {res['signal']}\n")
            if "cv_mean" in res:
                f.write(f"Model CV      : {res['cv_mean']:.2%} ± {res['cv_std']:.2%}\n")
            f.write("-----------------------------------\n")

    print("[OK] combined_forecast.txt created")


if __name__ == "__main__":
    main()
