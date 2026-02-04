from datetime import datetime


def convert_reservation_data(row: list) -> list:
    reservation_id = int(row[0])
    name = row[1]
    email = row[2]
    phone = row[3]

    reservation_date = datetime.strptime(row[4], "%Y-%m-%d").date()
    reservation_time = datetime.strptime(row[5], "%H:%M").time()

    duration_hours = int(row[6])
    price = float(row[7])
    confirmed = (row[8] == "True")

    reserved_resource = row[9]
    created_at = datetime.strptime(row[10], "%Y-%m-%d %H:%M:%S")

    return [
        reservation_id,
        name,
        email,
        phone,
        reservation_date,
        reservation_time,
        duration_hours,
        price,
        confirmed,
        reserved_resource,
        created_at
    ]

def confirmed_reservations(reservations: list) -> None:
    print("1) Confirmed Reservations")

    for r in reservations:
        if r[8]:
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {r[9]}, {date_str} at {time_str}")

    print()

def long_reservations(reservations: list) -> None:
    print("2) Long Reservations (≥ 3 h)")

    for r in reservations:
        if r[6] >= 3:
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {date_str} at {time_str}, duration {r[6]} h, {r[9]}")

    print()

def confirmation_statuses(reservations: list) -> None:
    print("3) Reservation Confirmation Status")

    for r in reservations:
        status = "Confirmed" if r[8] else "NOT Confirmed"
        print(f"{r[1]} → {status}")

    print()

def confirmation_summary(reservations: list) -> None:
    confirmed = 0
    not_confirmed = 0

    for r in reservations:
        if r[8]:
            confirmed += 1
        else:
            not_confirmed += 1

    print("4) Confirmation Summary")
    print(f"- Confirmed reservations: {confirmed} pcs")
    print(f"- Not confirmed reservations: {not_confirmed} pcs")
    print()

def total_revenue(reservations: list) -> None:
    total = 0.0

    for r in reservations:
        if r[8]:
            total += r[6] * r[7]

    amount_str = f"{total:.2f}".replace(".", ",")

    print("5) Total Revenue from Confirmed Reservations")
    print(f"Total revenue from confirmed reservations: {amount_str} €")

def main():
    reservations = []

    with open("reservations.txt", "r", encoding="utf-8") as file:
        for line in file:
            row = line.strip().split("|")
            reservations.append(convert_reservation_data(row))

    confirmed_reservations(reservations)
    long_reservations(reservations)
    confirmation_statuses(reservations)
    confirmation_summary(reservations)
    total_revenue(reservations)

if __name__ == "__main__":
    main()