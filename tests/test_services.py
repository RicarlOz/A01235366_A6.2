"""Unit tests for reservation system services."""

from __future__ import annotations

import io
import shutil
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout

from src.services import build_services


class TestReservationSystem(unittest.TestCase):
    """Tests covering hotel, customer and reservation behaviors."""

    def setUp(self) -> None:
        """
        Create an isolated temporary data directory and initialize services
        for each test.
        """
        self.data_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.data_dir)

        hotel_service, customer_service, res_service = build_services(
            self.data_dir
        )
        self.hotel_service = hotel_service
        self.customer_service = customer_service
        self.res_service = res_service

    def test_create_and_get_hotel(self) -> None:
        """Verify that a created hotel can be retrieved correctly."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        loaded = self.hotel_service.get_hotel(hotel.hotel_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(hotel.hotel_id, loaded.hotel_id)

    def test_modify_hotel(self) -> None:
        """Verify that hotel information can be modified successfully."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        ok = self.hotel_service.modify_hotel(hotel.hotel_id, name="H2")
        self.assertTrue(ok)

    def test_delete_hotel(self) -> None:
        """Verify that a hotel can be deleted successfully."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        ok = self.hotel_service.delete_hotel(hotel.hotel_id)
        self.assertTrue(ok)

    def test_create_and_modify_customer(self) -> None:
        """Verify that a customer can be created and modified."""
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")
        ok = self.customer_service.modify_customer(
            cust.customer_id,
            email="new@x.com"
        )
        self.assertTrue(ok)

    def test_create_reservation_and_cancel(self) -> None:
        """Verify that a reservation can be created and then cancelled."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 1)
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")

        reservation = self.res_service.create_reservation(
            hotel.hotel_id,
            cust.customer_id
        )
        self.assertIsNotNone(reservation)
        ok = self.res_service.cancel_reservation(reservation.reservation_id)
        self.assertTrue(ok)

    def test_negative_reservation_fails_if_customer_not_found(self) -> None:
        """Ensure reservation creation fails if the customer does not exist."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 1)
        buf = io.StringIO()
        with redirect_stdout(buf):
            reservation = self.res_service.create_reservation(
                hotel.hotel_id,
                "missing"
            )
        self.assertIsNone(reservation)
        self.assertIn("Customer not found", buf.getvalue())

    def test_negative_reservation_fails_if_hotel_not_found(self) -> None:
        """Ensure reservation creation fails if the hotel does not exist."""
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")
        buf = io.StringIO()
        with redirect_stdout(buf):
            reservation = self.res_service.create_reservation(
                "missing",
                cust.customer_id
            )
        self.assertIsNone(reservation)
        self.assertIn("Hotel not found", buf.getvalue())

    def test_negative_reservation_fails_when_full(self) -> None:
        """Ensure reservation fails when no rooms are available."""
        hotel = self.hotel_service.create_hotel("H1", "MTY", 1)
        cust1 = self.customer_service.create_customer("C1", "c1@x.com")
        cust2 = self.customer_service.create_customer("C2", "c2@x.com")

        r1 = self.res_service.create_reservation(
            hotel.hotel_id,
            cust1.customer_id
        )
        self.assertIsNotNone(r1)

        buf = io.StringIO()
        with redirect_stdout(buf):
            r2 = self.res_service.create_reservation(
                hotel.hotel_id,
                cust2.customer_id
            )
        self.assertIsNone(r2)
        self.assertIn("No rooms available", buf.getvalue())

    def test_negative_cancel_non_existing_reservation(self) -> None:
        """Ensure cancelling a non-existing reservation returns False."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = self.res_service.cancel_reservation("missing")
        self.assertFalse(ok)
        self.assertIn("Reservation not found", buf.getvalue())

    def test_negative_modify_customer_invalid_data(self) -> None:
        """Ensure modifying a customer with invalid data fails."""
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = self.customer_service.modify_customer(
                cust.customer_id,
                email="  "
            )
        self.assertFalse(ok)
        self.assertIn("Invalid customer modification data", buf.getvalue())

    def test_negative_invalid_json_in_file_is_handled(self) -> None:
        """Ensure invalid JSON in storage files is handled gracefully."""
        hotels_path = self.data_dir / "hotels.json"
        hotels_path.write_text("{ invalid json", encoding="utf-8")

        buf = io.StringIO()
        with redirect_stdout(buf):
            hotels = self.hotel_service.list_hotels()

        self.assertEqual([], hotels)
        self.assertIn("Invalid JSON", buf.getvalue())
