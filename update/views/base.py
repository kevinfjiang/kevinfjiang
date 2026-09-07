from abc import ABC, abstractmethod

from update.models import ReadmeData


class BaseView(ABC):
    """Abstract base class for all renderer views."""

    def __init__(self, data: ReadmeData) -> None:
        self.data = data

    @abstractmethod
    def generate(self) -> None:
        """Generate all relevant output files for this view."""
        pass
