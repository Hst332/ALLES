from gas_forecast import run_gas_forecast
from oil_forecast import run_oil_forecast

OUTPUT = "combined_forecast.txt"

def main():
    gas = run_gas_forecast()
    oil = run_oil_forecast()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(gas + "\n\n" + oil)

    print("[OK] combined_forecast.txt created")

if __name__ == "__main__":
    main()
