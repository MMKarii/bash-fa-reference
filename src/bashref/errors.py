from __future__ import annotations


class ReferenceErrorBase(Exception):
    """Base class for expected Bashref reference failures."""


class EntryNotFoundError(ReferenceErrorBase):
    def __init__(self, query: str, language: str):
        self.query = query
        self.language = language
        super().__init__(f"reference entry not found: {query}")


class CorruptReferenceError(ReferenceErrorBase):
    """Raised when packaged reference data cannot be trusted."""
