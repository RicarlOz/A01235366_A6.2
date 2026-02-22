"""Services implementing required behaviors for Hotel, Customer and Reservation."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from src.models import Customer, Hotel, Reservation
from src.storage import JsonStore


class HotelService:
    """Hotel operations + room reservation/cancellation (hotel perspective)."""

    def __init__(self, hotels_store: JsonStore, reservations_store: JsonStore) -> None:
        self._hotels_store = hotels_store
        self._reservations_store = reservations_store

    def create_hotel(self, name: str, location: str, total_rooms: int) -> Hotel:
        """Create and persist a new hotel."""
        hotel = Hotel(
            hotel_id=str(uuid4()),
            name=name.strip(),
            location=location.strip(),
            total_rooms=total_rooms,
        )
        hotels = self._hotels_store.load_entities(Hotel.from_dict)
        hotels.append(hotel)
        self._hotels_store.save_list([h.to_dict() for h in hotels])
        return hotel

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel by id."""
        hotels = self._hotels_store.load_entities(Hotel.from_dict)
        before = len(hotels)
        hotels = [h for h in hotels if h.hotel_id != hotel_id]
        self._hotels_store.save_list([h.to_dict() for h in hotels])
        return len(hotels) != before

    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        """Get hotel information by id."""
        hotels = self._hotels_store.load_entities(Hotel.from_dict)
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                return hotel
        return None

    def list_hotels(self) -> List[Hotel]:
        """Return all hotels."""
        return self._hotels_store.load_entities(Hotel.from_dict)

    def modify_hotel(
        self,
        hotel_id: str,
        name: Optional[str] = None,
        location: Optional[str] = None,
        total_rooms: Optional[int] = None,
    ) -> bool:
        """Modify hotel fields (partial update)."""
        hotels = self._hotels_store.load_entities(Hotel.from_dict)
        updated: List[Hotel] = []
        changed = False

        for hotel in hotels:
            if hotel.hotel_id != hotel_id:
                updated.append(hotel)
                continue

            new_name = hotel.name if name is None else name.strip()
            new_location = hotel.location if location is None else location.strip()
            new_total_rooms = hotel.total_rooms if total_rooms is None else total_rooms

            if not new_name or not new_location or new_total_rooms < 1:
                print("[ERROR] Invalid hotel modification data.")
                updated.append(hotel)
                continue

            updated.append(
                Hotel(
                    hotel_id=hotel.hotel_id,
                    name=new_name,
                    location=new_location,
                    total_rooms=new_total_rooms,
                )
            )
            changed = True

        self._hotels_store.save_list([h.to_dict() for h in updated])
        return changed

    def reserve_room(self, hotel_id: str, customer_id: str) -> Optional[Reservation]:
        """Reserve 1 room in a hotel; create an ACTIVE reservation if available."""
        hotel = self.get_hotel(hotel_id)
        if hotel is None:
            print("[ERROR] Hotel not found.")
            return None

        reservations = self._reservations_store.load_entities(Reservation.from_dict)
        active_count = sum(
            1 for r in reservations if r.hotel_id == hotel_id and r.is_active()
        )
        if active_count >= hotel.total_rooms:
            print("[ERROR] No rooms available.")
            return None

        reservation = Reservation(
            reservation_id=str(uuid4()),
            hotel_id=hotel_id,
            customer_id=customer_id,
            status="ACTIVE",
        )
        reservations.append(reservation)
        self._reservations_store.save_list([r.to_dict() for r in reservations])
        return reservation

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation (set status to CANCELLED)."""
        reservations = self._reservations_store.load_entities(Reservation.from_dict)
        updated: List[Reservation] = []
        changed = False

        for res in reservations:
            if res.reservation_id == reservation_id and res.is_active():
                updated.append(res.cancelled())
                changed = True
            else:
                updated.append(res)

        if not changed:
            print("[ERROR] Reservation not found or already cancelled.")

        self._reservations_store.save_list([r.to_dict() for r in updated])
        return changed


class CustomerService:
    """Customer CRUD operations."""

    def __init__(self, customers_store: JsonStore) -> None:
        self._customers_store = customers_store

    def create_customer(self, name: str, email: str) -> Customer:
        """Create and persist a new customer."""
        customer = Customer(
            customer_id=str(uuid4()),
            name=name.strip(),
            email=email.strip(),
        )
        customers = self._customers_store.load_entities(Customer.from_dict)
        customers.append(customer)
        self._customers_store.save_list([c.to_dict() for c in customers])
        return customer

    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer by id."""
        customers = self._customers_store.load_entities(Customer.from_dict)
        before = len(customers)
        customers = [c for c in customers if c.customer_id != customer_id]
        self._customers_store.save_list([c.to_dict() for c in customers])
        return len(customers) != before

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer information by id."""
        customers = self._customers_store.load_entities(Customer.from_dict)
        for customer in customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def modify_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> bool:
        """Modify customer fields (partial update)."""
        customers = self._customers_store.load_entities(Customer.from_dict)
        updated: List[Customer] = []
        changed = False

        for customer in customers:
            if customer.customer_id != customer_id:
                updated.append(customer)
                continue

            new_name = customer.name if name is None else name.strip()
            new_email = customer.email if email is None else email.strip()
            if not new_name or not new_email:
                print("[ERROR] Invalid customer modification data.")
                updated.append(customer)
                continue

            updated.append(
                Customer(
                    customer_id=customer.customer_id,
                    name=new_name,
                    email=new_email,
                )
            )
            changed = True

        self._customers_store.save_list([c.to_dict() for c in updated])
        return changed

    def list_customers(self) -> List[Customer]:
        """Return all customers."""
        return self._customers_store.load_entities(Customer.from_dict)


class ReservationService:
    """Reservation behaviors (create/cancel) as an explicit abstraction."""

    def __init__(
        self,
        reservations_store: JsonStore,
        hotel_service: HotelService,
        customer_service: CustomerService,
    ) -> None:
        self._reservations_store = reservations_store
        self._hotel_service = hotel_service
        self._customer_service = customer_service

    def create_reservation(self, hotel_id: str, customer_id: str) -> Optional[Reservation]:
        """Create reservation if hotel and customer exist and there is availability."""
        customer = self._customer_service.get_customer(customer_id)
        if customer is None:
            print("[ERROR] Customer not found.")
            return None
        return self._hotel_service.reserve_room(hotel_id, customer_id)

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel reservation by id."""
        return self._hotel_service.cancel_reservation(reservation_id)

    def list_reservations(self) -> List[Reservation]:
        """Return all reservations (including cancelled)."""
        return self._reservations_store.load_entities(Reservation.from_dict)


def build_services(
    data_dir: Path,
) -> tuple[HotelService, CustomerService, ReservationService]:
    """Factory to build services pointing to a given data directory."""
    hotels_store = JsonStore(data_dir / "hotels.json")
    customers_store = JsonStore(data_dir / "customers.json")
    reservations_store = JsonStore(data_dir / "reservations.json")

    hotel_service = HotelService(hotels_store, reservations_store)
    customer_service = CustomerService(customers_store)
    reservation_service = ReservationService(
        reservations_store, hotel_service, customer_service
    )
    return hotel_service, customer_service, reservation_service
