import logging

import httpx

from app.config import settings
from app.platforms.base import BasePlatform

logger = logging.getLogger(__name__)


class MastodonPlatform(BasePlatform):
    """Publish messages to a Mastodon instance."""

    platform_name = "mastodon"

    async def publish(self, message: str) -> dict:
        """Publish a public status to Mastodon."""

        if not settings.mastodon_instance_url:
            raise ValueError("Mastodon instance URL is not configured.")

        if not settings.mastodon_access_token:
            raise ValueError("Mastodon access token is not configured.")

        instance_url = settings.mastodon_instance_url.rstrip("/")
        api_url = f"{instance_url}/api/v1/statuses"

        headers = {"Authorization": (f"Bearer {settings.mastodon_access_token}")}

        payload = {
            "status": message,
            "visibility": "public",
        }

        try:
            logger.info("Publishing status to Mastodon.")

            async with httpx.AsyncClient(
                timeout=20.0,
                trust_env=True,
            ) as client:
                response = await client.post(
                    api_url,
                    headers=headers,
                    data=payload,
                )
                response.raise_for_status()
                result = response.json()

            post_id = result["id"]

            logger.info(
                "Mastodon status published successfully. " "Post ID: %s",
                post_id,
            )

            return {
                "platform": self.platform_name,
                "status": "success",
                "post_id": post_id,
                "posted_url": result.get("url"),
                "public_access": True,
            }

        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
        ):
            logger.exception("Mastodon publishing failed.")
            raise
