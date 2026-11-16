import logging

import httpx

from app.config import settings
from app.platforms.base import BasePlatform

logger = logging.getLogger(__name__)


class DevToPlatform(BasePlatform):
    """Publish articles to DEV.to."""

    platform_name = "devto"

    async def publish(self, message: str) -> dict:
        """Create and publish an article on DEV.to."""

        if not settings.devto_api_key:
            raise ValueError("DEV.to API key is not configured.")

        api_url = "https://dev.to/api/articles"

        headers = {
            "api-key": settings.devto_api_key,
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": "AutomatedMultiPlatformPosting/1.0",
        }

        payload = {
            "article": {
                "title": "Automated Multi-Platform Posting",
                "body_markdown": message,
                "published": True,
            }
        }

        try:
            logger.info("Publishing article to DEV.to.")

            async with httpx.AsyncClient(
                timeout=30.0,
                trust_env=True,
            ) as client:
                response = await client.post(
                    api_url,
                    headers=headers,
                    json=payload,
                )
                if response.status_code >= 400:
                    logger.error(
                        "DEV.to response: %s",
                        response.text,
                    )
                response.raise_for_status()
                result = response.json()

            article_id = result["id"]

            logger.info(
                "DEV.to article published successfully. " "Article ID: %s",
                article_id,
            )

            return {
                "platform": self.platform_name,
                "status": "success",
                "article_id": article_id,
                "posted_url": result.get("url"),
                "public_access": True,
            }

        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
        ):
            logger.exception("DEV.to publishing failed.")
            raise
