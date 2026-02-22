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