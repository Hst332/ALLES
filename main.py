from gas_forecast import train_and_predict
from oil_forecast import build_signal

OUT_FILE = "combined_forecast.txt"


def write_section(res, f):
    f.write("===================================\n")
    f.write(f"{res['section']}\n")
    f.write("===================================\n")
    f.write(f"Run time (UTC): {res['run_time']}\n")
    f.write(f"Data date     : {res['data_date']}\n\n")

    if "brent" in res:
        f.write(f"Brent Close   : {res['brent']:.2f}\n")
        f.write(f"WTI Close     : {res['wti']:.2f}\n")
        f.write(f"Spread        : {res['spread']:.2f}\n\n")
    else:
        f.write(f"Model CV      : {res['cv_mean']:.2%} ± {res['cv_std']:.2%}\n\n")

    f.write(f"Prob UP       : {res['prob_up']:.2%}\n")
    f.write(f"Prob DOWN     : {res['prob_down']:.2%}\n")
    f.write(f"Signal        : {res['signal']}\n")
    f.write("===================================\n\n")


def main():
    gas = train_and_predict()
    oil = build_signal()

    with open(OUT_FILE, "w") as f:
        write_section(gas, f)
        write_section(oil, f)

    print("[OK] combined_forecast.txt created")


if __name__ == "__main__":
    main()
