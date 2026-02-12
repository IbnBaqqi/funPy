# Copyright (c) 2026 Salaudeen Abdulbaki
# License: MIT

import csv
from datetime import datetime, date
from typing import Dict, List, Tuple


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
    Reads a CSV file and returns a list of parsed rows.
    Each row contains datetime, consumption list, and production list.
    """
    rows: List[Dict] = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # skip header

        for row in reader:
            rows.append({
                "datetime": datetime.fromisoformat(row[0]),
                "consumption": [int(row[1]), int(row[2]), int(row[3])],
                "production": [int(row[4]), int(row[5]), int(row[6])]
            })

    return rows


def calculate_daily_totals(rows: List[Dict]) -> Dict[date, Dict]:
    """
    Groups hourly rows by date and calculates daily totals (Wh).
    """
    daily: Dict[date, Dict] = {}

    for row in rows:
        day: date = row["datetime"].date()

        if day not in daily:
            daily[day] = {
                "consumption": [0, 0, 0],
                "production": [0, 0, 0]
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
    Formats kWh value with two decimals and comma decimal separator.
    """
    return f"{value_kwh:.2f}".replace(".", ",")


def format_week_section(week_number: int, daily_data: Dict[date, Dict]) -> str:
    """
    Formats one week's daily totals into a structured text section.
    Returns the formatted string.
    """
    lines: List[str] = []

    lines.append(f"Week {week_number} electricity consumption and production (kWh, by phase)")
    lines.append("")
    lines.append("Day        Date         Consumption [kWh]            Production [kWh]")
    lines.append("                         v1      v2      v3           v1     v2     v3")
    lines.append("-" * 75)

    for day in sorted(daily_data.keys()):
        weekday = FINNISH_WEEKDAYS[day.weekday()]
        date_str = day.strftime("%d.%m.%Y")

        cons = [wh_to_kwh(v) for v in daily_data[day]["consumption"]]
        prod = [wh_to_kwh(v) for v in daily_data[day]["production"]]

        cons_str = [format_kwh(v) for v in cons]
        prod_str = [format_kwh(v) for v in prod]

        line = (
            f"{weekday:<10} {date_str:<12} "
            f"{cons_str[0]:>6}  {cons_str[1]:>6}  {cons_str[2]:>6}      "
            f"{prod_str[0]:>5}  {prod_str[1]:>5}  {prod_str[2]:>5}"
        )

        lines.append(line)

    lines.append("\n")
    return "\n".join(lines)


def write_report(filename: str, content: str) -> None:
    """
    Writes the final formatted report to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def main() -> None:
    """
    Main function:
    - Reads three weekly CSV files
    - Computes daily summaries
    - Writes formatted report to summary.txt
    """
    weeks: List[Tuple[int, str]] = [
        (41, "week41.csv"),
        (42, "week42.csv"),
        (43, "week43.csv")
    ]

    full_report: List[str] = []

    for week_number, filename in weeks:
        rows = read_data(filename)
        daily_totals = calculate_daily_totals(rows)
        week_section = format_week_section(week_number, daily_totals)
        full_report.append(week_section)

    final_text = "\n".join(full_report)

    write_report("summary.txt", final_text)

    print("Report successfully written to summary.txt")


if __name__ == "__main__":
    main()
