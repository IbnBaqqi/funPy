from datetime import datetime


def print_reservation_number(reservation: list) -> None:
    """Print reservation number"""
    reservation_number = int(reservation[0])
    print(f"Reservation number: {reservation_number}")


def print_booker(reservation: list) -> None:
    """Print booker name"""
    print(f"Booker: {reservation[1]}")


def print_date(reservation: list) -> None:
    """Print reservation date"""
    day = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    finnish_day = day.strftime("%d.%m.%Y")
    print(f"Date: {finnish_day}")


def print_start_time(reservation: list) -> None:
    """Print start time"""
    time = datetime.strptime(reservation[3], "%H:%M").time()
    finnish_time = time.strftime("%H.%M")
    print(f"Start time: {finnish_time}")


def print_hours(reservation: list) -> None:
    """Print number of hours"""
    hours = int(reservation[4])
    print(f"Number of hours: {hours}")


def print_hourly_rate(reservation: list) -> None:
    """Print hourly price"""
    hourly_price = float(reservation[5])
    price = f"{hourly_price:.2f}".replace(".", ",")
    print(f"Hourly price: {price} €")


def print_total_price(reservation: list) -> None:
    """Print total price"""
    hours = int(reservation[4])
    hourly_price = float(reservation[5])
    total = hours * hourly_price
    total_price = f"{total:.2f}".replace(".", ",")
    print(f"Total price: {total_price} €")


def print_paid(reservation: list) -> None:
    """Print payment status"""
    paid = reservation[6] == "True"
    print(f"Paid: {'Yes' if paid else 'No'}")


def print_venue(reservation: list) -> None:
    """Print location"""
    print(f"Location: {reservation[7]}")


def print_phone(reservation: list) -> None:
    """Print phone number"""
    print(f"Phone: {reservation[8]}")


def print_email(reservation: list) -> None:
    """Print email"""
    print(f"Email: {reservation[9]}")


def main():
    with open("reservations.txt", "r", encoding="utf-8") as file:
        reservation = file.read().strip()

    reservation = reservation.split("|")

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_rate(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_venue(reservation)
    print_phone(reservation)
    print_email(reservation)


if __name__ == "__main__":
    main()
