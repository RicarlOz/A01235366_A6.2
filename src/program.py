"""Simple console program demonstrating the reservation system."""

from __future__ import annotations

from pathlib import Path

from src.services import build_services


def main() -> None:
    """Run a small interactive demo."""
    data_dir = Path("data")
    hotel_service, customer_service, reservation_service = build_services(data_dir)

    print("Reservation System Demo")
    print("1) Create hotel")
    print("2) Create customer")
    print("3) Create reservation")
    print("4) Cancel reservation")
    print("5) List hotels/customers/reservations")
    print("0) Exit")

    while True:
        option = input("Select option: ").strip()

        if option == "0":
            break
        if option == "1":
            handle_create_hotel(hotel_service)
        elif option == "2":
            handle_create_customer(customer_service)
        elif option == "3":
            handle_create_reservation(reservation_service)
        elif option == "4":
            handle_cancel_reservation(reservation_service)
        elif option == "5":
            print("Hotels:")
            for hotel in hotel_service.list_hotels():
                print(hotel)
            print("Customers:")
            for customer in customer_service.list_customers():
                print(customer)
            print("Reservations:")
            for reservation in reservation_service.list_reservations():
                print(reservation)
        else:
            print("[ERROR] Invalid option")


def handle_create_hotel(hotel_service):
    """Handle user input for creating a hotel."""
    name = input("Hotel name: ")
    location = input("Location: ")
    total_rooms = int(input("Total rooms: "))
    hotel = hotel_service.create_hotel(name, location, total_rooms)
    print(f"Created hotel: {hotel.hotel_id}")


def handle_create_customer(customer_service):
    """Handle user input for creating a customer."""
    name = input("Customer name: ")
    email = input("Email: ")
    customer = customer_service.create_customer(name, email)
    print(f"Created customer: {customer.customer_id}")


def handle_create_reservation(reservation_service):
    """Handle user input for creating a reservation."""
    hotel_id = input("Hotel id: ").strip()
    customer_id = input("Customer id: ").strip()
    reservation = reservation_service.create_reservation(hotel_id, customer_id)
    if reservation is not None:
        print(f"Created reservation: {reservation.reservation_id}")


def handle_cancel_reservation(reservation_service):
    """Handle user input for cancelling a reservation."""
    reservation_id = input("Reservation id: ").strip()
    ok = reservation_service.cancel_reservation(reservation_id)
    print("Cancelled" if ok else "Not cancelled")

if __name__ == "__main__":
    main()
