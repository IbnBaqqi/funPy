import csv
from datetime import datetime, date
from typing import Dict, List


FINNISH_WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def read_data(filename: str) -> List[Dict]:
    """
    Reads the CSV file and returns a list of rows with parsed datetime and values.
    """
    rows = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        for row in reader:
            rows.append({
                "datetime": datetime.fromisoformat(row[0]),
                "consumption": [int(row[1]), int(row[2]), int(row[3])],
                "production": [int(row[4]), int(row[5]), int(row[6])],
            })

    return rows


def calculate_daily_totals(rows: List[Dict]) -> Dict[date, Dict]:
    """
    Groups hourly rows by date and calculates daily totals in Wh.
    """
    daily: Dict[date, Dict] = {}

    for row in rows:
        day = row["datetime"].date()

        if day not in daily:
            daily[day] = {
                "consumption": [0, 0, 0],
                "production": [0, 0, 0],
            }

        for i in range(3):
            daily[day]["consumption"][i] += row["consumption"][i]
            daily[day]["production"][i] += row["production"][i]

    return daily


def wh_to_kwh(value_wh: int) -> float:
    """
    Converts watt-hours to kilowatt-hours.
    """
    return value_wh / 1000.0


def format_kwh(value_kwh: float) -> str:
    """
    Formats kWh value with two decimals and decimal comma.
    """
    return f"{value_kwh:.2f}".replace(".", ",")


def print_table(daily_data: Dict[date, Dict]) -> None:
    """
    Prints the weekly electricity consumption and production table.
    """
    print("Week 42 electricity consumption and production (kWh, by phase)\n")

    header = (
        "Day          Date        "
        "Consumption [kWh]               "
        "Production [kWh]\n"
        "             (dd.mm.yyyy)  "
        "v1      v2      v3           "
        "v1     v2     v3\n"
        + "-" * 75
    )
    print(header)

    for day in sorted(daily_data.keys()):
        weekday = FINNISH_WEEKDAYS[day.weekday()]
        date_str = day.strftime("%d.%m.%Y")

        cons = [wh_to_kwh(v) for v in daily_data[day]["consumption"]]
        prod = [wh_to_kwh(v) for v in daily_data[day]["production"]]

        cons_str = [format_kwh(v) for v in cons]
        prod_str = [format_kwh(v) for v in prod]

        print(
            f"{weekday:<12} {date_str}   "
            f"{cons_str[0]:>6}  {cons_str[1]:>6}  {cons_str[2]:>6}       "
            f"{prod_str[0]:>5}  {prod_str[1]:>5}  {prod_str[2]:>5}"
        )


def main() -> None:
    """
    Main function: reads data, computes daily totals, and prints the report.
    """
    rows = read_data("week42.csv")
    daily_totals = calculate_daily_totals(rows)
    print_table(daily_totals)


if __name__ == "__main__":
    main()
