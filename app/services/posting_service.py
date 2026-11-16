import asyncio
import logging
from datetime import UTC, datetime

from app.platforms.bluesky import BlueskyPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.telegraph import TelegraphPlatform

logger = logging.getLogger(__name__)


async def publish_to_platform(
    platform,
    message: str,
) -> dict:
    """Publish to one platform and capture its result."""

    try:
        result = await platform.publish(message)
        timestamp = datetime.now(UTC)

        logger.info(
            "Publishing succeeded on %s.",
            platform.platform_name,
        )

        return {
            "platform": platform.platform_name,
            "status": "success",
            "posted_url": result.get("posted_url"),
            "public_access": result.get("public_access"),
            "date": timestamp.date().isoformat(),
            "time": timestamp.time().isoformat(),
            "timezone": "UTC",
            "error": None,
        }

    except Exception:
        timestamp = datetime.now(UTC)

        logger.exception(
            "Publishing failed on %s.",
            platform.platform_name,
        )

        return {
            "platform": platform.platform_name,
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": timestamp.date().isoformat(),
            "time": timestamp.time().isoformat(),
            "timezone": "UTC",
            "error": (
                "Publishing failed. Check application " "configuration and logs."
            ),
        }


async def publish_to_all_platforms(
    message: str,
) -> list[dict]:
    """Publish a message to all configured platforms."""

    platforms = [
        TelegramPlatform(),
        MastodonPlatform(),
        TelegraphPlatform(),
        DevToPlatform(),
        BlueskyPlatform(),
    ]

    tasks = [publish_to_platform(platform, message) for platform in platforms]

    return await asyncio.gather(*tasks)
