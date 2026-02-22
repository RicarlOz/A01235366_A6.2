"""Domain models for the reservation system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


def _require_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Invalid '{field_name}': must be a non-empty string.")
    return value.strip()


def _require_int(value: Any, field_name: str, min_value: int = 0) -> int:
    if not isinstance(value, int) or value < min_value:
        raise ValueError(f"Invalid '{field_name}': must be an int >= {min_value}.")
    return value


@dataclass(frozen=True)
class Hotel:
    """Represents a hotel entity."""
    hotel_id: str
    name: str
    location: str
    total_rooms: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Hotel":
        """Create a Hotel from a dict, validating required fields."""
        hotel_id = _require_str(data.get("hotel_id"), "hotel_id")
        name = _require_str(data.get("name"), "name")
        location = _require_str(data.get("location"), "location")
        total_rooms = _require_int(data.get("total_rooms"), "total_rooms", 1)
        return Hotel(
            hotel_id=hotel_id,
            name=name,
            location=location,
            total_rooms=total_rooms,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize hotel to dict."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
        }


@dataclass(frozen=True)
class Customer:
    """Represents a customer entity."""
    customer_id: str
    name: str
    email: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Customer":
        """Create a Customer from a dict, validating required fields."""
        customer_id = _require_str(data.get("customer_id"), "customer_id")
        name = _require_str(data.get("name"), "name")
        email = _require_str(data.get("email"), "email")
        return Customer(customer_id=customer_id, name=name, email=email)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize customer to dict."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }


@dataclass(frozen=True)
class Reservation:
    """Represents a reservation: a customer reserves 1 room in a hotel."""
    reservation_id: str
    hotel_id: str
    customer_id: str
    status: str = "ACTIVE"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Reservation":
        """Create a Reservation from a dict, validating required fields."""
        reservation_id = _require_str(data.get("reservation_id"), "reservation_id")
        hotel_id = _require_str(data.get("hotel_id"), "hotel_id")
        customer_id = _require_str(data.get("customer_id"), "customer_id")
        status = data.get("status", "ACTIVE")
        status_str = _require_str(status, "status")
        if status_str not in {"ACTIVE", "CANCELLED"}:
            raise ValueError("Invalid 'status': must be ACTIVE or CANCELLED.")
        return Reservation(
            reservation_id=reservation_id,
            hotel_id=hotel_id,
            customer_id=customer_id,
            status=status_str,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize reservation to dict."""
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id,
            "status": self.status,
        }

    def is_active(self) -> bool:
        """Return True if reservation is active."""
        return self.status == "ACTIVE"

    def cancelled(self) -> "Reservation":
        """Return a copy of the reservation with CANCELLED status."""
        return Reservation(
            reservation_id=self.reservation_id,
            hotel_id=self.hotel_id,
            customer_id=self.customer_id,
            status="CANCELLED",
        )
