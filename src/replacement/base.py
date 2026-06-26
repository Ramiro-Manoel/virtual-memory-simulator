"""Replacement policy interface (Strategy pattern — Open/Closed Principle)."""

from abc import ABC, abstractmethod


class ReplacementPolicy(ABC):
    """Decides which frame to remove. Works only with frame numbers."""

    @abstractmethod
    def record_load(self, frame_number: int) -> None:
        """A page was just loaded into this frame."""

    @abstractmethod
    def record_access(self, frame_number: int) -> None:
        """This frame was accessed (a page hit)."""

    @abstractmethod
    def choose_victim(self) -> int:
        """Return the frame number to remove (and forget it)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Algorithm name shown in the output."""
