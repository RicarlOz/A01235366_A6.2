"""JSON file storage with resilient error handling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar("T")


class JsonStore:
    """Stores a list of entities (dicts) in a JSON file.

    Requirement: Handle invalid data in the file. Errors are printed and
    execution continues (returns empty list or skips invalid entries).
    """

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load_list(self) -> List[Dict[str, Any]]:
        """Load a list of dicts from the JSON file."""
        if not self._file_path.exists():
            return []

        try:
            raw = self._file_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"[ERROR] Invalid JSON in {self._file_path}: {exc}")
            return []
        except OSError as exc:
            print(f"[ERROR] Could not read {self._file_path}: {exc}")
            return []

        if not isinstance(data, list):
            print(
                f"[ERROR] Invalid data in {self._file_path}: expected a list."
                )
            return []

        valid_items: List[Dict[str, Any]] = []
        for item in data:
            if isinstance(item, dict):
                valid_items.append(item)
            else:
                path = self._file_path
                print(f"[ERROR] Invalid item in {path}: expected dict.")
        return valid_items

    def save_list(self, items: List[Dict[str, Any]]) -> None:
        """Persist a list of dicts to the JSON file."""
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            self._file_path.write_text(
                json.dumps(items, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"[ERROR] Could not write {self._file_path}: {exc}")

    def load_entities(self, factory: Callable[[Dict[str, Any]], T]) -> List[T]:
        """Load entities using a factory; skip invalid entities."""
        entities: List[T] = []
        for item in self.load_list():
            try:
                entities.append(factory(item))
            except ValueError as exc:
                print(f"[ERROR] Invalid entity in {self._file_path}: {exc}")
        return entities
