from datetime import datetime


def main():
    with open("reservations.txt", "r", encoding="utf-8") as file:
        line = file.readline().strip()

    reservation = line.split("|")

    reservation_number = int(reservation[0])
    booker = reservation[1]

    day = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    finnish_day = day.strftime("%d.%m.%Y")

    start_time = datetime.strptime(reservation[3], "%H:%M").time()
    finnish_time = start_time.strftime("%H.%M")

    hours = int(reservation[4])
    hourly_price = float(reservation[5])
    total_price = hours * hourly_price

    paid = reservation[6] == "True"

    resource = reservation[7]
    phone = reservation[8]
    email = reservation[9]

    print(f"Reservation number: {reservation_number}")
    print(f"Booker: {booker}")
    print(f"Date: {finnish_day}")
    print(f"Start time: {finnish_time}")
    print(f"Number of hours: {hours}")
    print(f"Hourly price: {hourly_price:.2f}".replace(".", ",") + " €")
    print(f"Total price: {total_price:.2f}".replace(".", ",") + " €")
    print(f"Paid: {'Yes' if paid else 'No'}")
    print(f"Location: {resource}")
    print(f"Phone: {phone}")
    print(f"Email: {email}")


if __name__ == "__main__":
    main()
