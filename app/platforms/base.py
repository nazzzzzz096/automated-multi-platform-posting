from abc import ABC, abstractmethod


class BasePlatform(ABC):
    """Common interface for all publishing platforms."""

    platform_name: str

    @abstractmethod
    async def publish(self, message: str) -> dict:
        """Publish a message to the platform."""
        ...
