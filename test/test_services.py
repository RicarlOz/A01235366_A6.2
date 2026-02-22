"""Unit tests for reservation system services."""

# pylint: disable=missing-function-docstring

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from src.services import build_services


class TestReservationSystem(unittest.TestCase):
    """Tests covering hotel, customer and reservation behaviors."""

    def setUp(self) -> None:
        self.data_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.data_dir)

        hotel_service, customer_service, res_service = build_services(
            self.data_dir
        )
        self.hotel_service = hotel_service
        self.customer_service = customer_service
        self.res_service = res_service

    def test_create_and_get_hotel(self) -> None:
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        loaded = self.hotel_service.get_hotel(hotel.hotel_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(hotel.hotel_id, loaded.hotel_id)

    def test_modify_hotel(self) -> None:
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        ok = self.hotel_service.modify_hotel(hotel.hotel_id, name="H2")
        self.assertTrue(ok)

    def test_delete_hotel(self) -> None:
        hotel = self.hotel_service.create_hotel("H1", "MTY", 2)
        ok = self.hotel_service.delete_hotel(hotel.hotel_id)
        self.assertTrue(ok)

    def test_create_and_modify_customer(self) -> None:
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")
        ok = self.customer_service.modify_customer(
            cust.customer_id,
            email="new@x.com"
            )
        self.assertTrue(ok)

    def test_create_reservation_and_cancel(self) -> None:
        hotel = self.hotel_service.create_hotel("H1", "MTY", 1)
        cust = self.customer_service.create_customer("Ricardo", "r@x.com")

        reservation = self.res_service.create_reservation(
            hotel.hotel_id,
            cust.customer_id
            )
        self.assertIsNotNone(reservation)
        ok = self.res_service.cancel_reservation(reservation.reservation_id)
        self.assertTrue(ok)
