"""Unit tests for JsonStore error handling paths."""

# pylint: disable=missing-function-docstring

from __future__ import annotations

import io
import json
import tempfile
import shutil
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.models import Hotel
from src.storage import JsonStore


class TestJsonStore(unittest.TestCase):
    """Tests focused on JsonStore resilience and error handling."""

    def setUp(self) -> None:
        self.data_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.data_dir)

        self.file_path = self.data_dir / "store.json"
        self.store = JsonStore(self.file_path)

    def test_load_list_returns_empty_when_file_missing(self) -> None:
        self.assertEqual([], self.store.load_list())

    def test_load_list_handles_non_list_json(self) -> None:
        self.file_path.write_text(json.dumps({"a": 1}), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            items = self.store.load_list()
        self.assertEqual([], items)
        self.assertIn("expected a list", buf.getvalue())

    def test_load_list_skips_non_dict_items(self) -> None:
        self.file_path.write_text(
            json.dumps([{"ok": True}, 123, "x"]),
            encoding="utf-8"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            items = self.store.load_list()
        self.assertEqual([{"ok": True}], items)
        self.assertIn("expected dict", buf.getvalue())

    def test_load_list_handles_os_error_on_read(self) -> None:
        """It should print an error and return [] when file read fails."""
        # Ensure file exists so it passes the exists() check
        self.file_path.write_text("[]", encoding="utf-8")

        buf = io.StringIO()
        with patch("src.storage.Path.read_text", side_effect=OSError("boom")):
            with redirect_stdout(buf):
                items = self.store.load_list()

        self.assertEqual([], items)
        self.assertIn("Could not read", buf.getvalue())

    def test_save_list_handles_os_error_on_write(self) -> None:
        with patch.object(Path, "write_text", side_effect=OSError("boom")):
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.store.save_list([{"a": 1}])
        self.assertIn("Could not write", buf.getvalue())

    def test_load_entities_skips_invalid_entities(self) -> None:
        # One valid hotel dict and one invalid hotel dict (missing fields)
        self.file_path.write_text(
            json.dumps(
                [
                    {
                        "hotel_id": "h1",
                        "name": "Hotel",
                        "location": "MTY",
                        "total_rooms": 1,
                    },
                    {"hotel_id": "h2"},
                ]
            ),
            encoding="utf-8",
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            hotels = self.store.load_entities(Hotel.from_dict)

        self.assertEqual(1, len(hotels))
        self.assertIn("Invalid entity", buf.getvalue())
