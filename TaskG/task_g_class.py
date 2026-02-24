from datetime import datetime


class Reservation:
    def __init__(
        self,
        reservation_id: int,
        name: str,
        email: str,
        phone: str,
        reservation_date,
        reservation_time,
        duration_hours: int,
        price: float,
        confirmed: bool,
        reserved_resource: str,
        created_at,
    ):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.duration_hours = duration_hours
        self.price = price
        self.confirmed = confirmed
        self.reserved_resource = reserved_resource
        self.created_at = created_at

    def is_confirmed(self) -> bool:
        return self.confirmed

    def is_long(self) -> bool:
        return self.duration_hours >= 3

    def total_price(self) -> float:
        return self.duration_hours * self.price


def convert_reservation_data(reservation: list[str]) -> Reservation:
    return Reservation(
        reservation_id=int(reservation[0]),
        name=reservation[1],
        email=reservation[2],
        phone=reservation[3],
        reservation_date=datetime.strptime(reservation[4], "%Y-%m-%d").date(),
        reservation_time=datetime.strptime(reservation[5], "%H:%M").time(),
        duration_hours=int(reservation[6]),
        price=float(reservation[7]),
        confirmed=True if reservation[8].strip() == "True" else False,
        reserved_resource=reservation[9],
        created_at=datetime.strptime(
            reservation[10].strip(), "%Y-%m-%d %H:%M:%S"
        ),
    )


def fetch_reservations(reservation_file: str) -> list[Reservation]:
    reservations = []

    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip()) > 0:
                fields = line.split("|")
                reservations.append(convert_reservation_data(fields))

    return reservations


def confirmed_reservations(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        if reservation.is_confirmed():
            print(
                f'- {reservation.name}, '
                f'{reservation.reserved_resource}, '
                f'{reservation.reservation_date.strftime("%d.%m.%Y")} '
                f'at {reservation.reservation_time.strftime("%H.%M")}'
            )


def long_reservations(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        if reservation.is_long():
            print(
                f'- {reservation.name}, '
                f'{reservation.reservation_date.strftime("%d.%m.%Y")} '
                f'at {reservation.reservation_time.strftime("%H.%M")}, '
                f'duration {reservation.duration_hours} h, '
                f'{reservation.reserved_resource}'
            )


def confirmation_statuses(reservations: list[Reservation]) -> None:
    for reservation in reservations:
        print(
            f'{reservation.name} → '
            f'{"Confirmed" if reservation.is_confirmed() else "NOT Confirmed"}'
        )


def confirmation_summary(reservations: list[Reservation]) -> None:
    confirmed_count = len([r for r in reservations if r.is_confirmed()])
    print(
        f'- Confirmed reservations: {confirmed_count} pcs\n'
        f'- Not confirmed reservations: {len(reservations) - confirmed_count} pcs'
    )


def total_revenue(reservations: list[Reservation]) -> None:
    revenue = sum(
        r.total_price()
        for r in reservations
        if r.is_confirmed()
    )
    print(
        f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace(".", ",")
    )


def main():
    reservations = fetch_reservations("reservations.txt")

    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)

    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)

    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)

    print("4) Confirmation Summary")
    confirmation_summary(reservations)

    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()