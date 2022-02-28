
"""Exceptions for Flipr."""

from typing import Any


class FliprError(Exception):
    """Error from Flipr api."""

    def __init__(self, *args: Any) -> None:
        """Initialize the exception."""
        Exception.__init__(self, *args)