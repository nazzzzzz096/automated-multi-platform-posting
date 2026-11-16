import asyncio
import json
import logging
import re

import httpx

from app.config import settings
from app.platforms.base import BasePlatform

logger = logging.getLogger(__name__)


def create_content_nodes(message: str) -> list:
    """Convert a message into Telegraph content nodes."""

    url_pattern = r"https?://[^\s<>]+"
    match = re.search(url_pattern, message)

    if not match:
        return [
            {
                "tag": "p",
                "children": [message],
            }
        ]

    url = match.group()
    clean_url = url.rstrip(".,!?;:)")

    start = match.start()
    end = start + len(clean_url)

    children = []

    if start > 0:
        children.append(message[:start])

    children.append(
        {
            "tag": "a",
            "attrs": {"href": clean_url},
            "children": [clean_url],
        }
    )

    if end < len(message):
        children.append(message[end:])

    return [
        {
            "tag": "p",
            "children": children,
        }
    ]


class TelegraphPlatform(BasePlatform):
    """Publish messages as Telegraph pages."""

    platform_name = "telegraph"

    async def publish(self, message: str) -> dict:
        """Create a public Telegraph page."""

        if not settings.telegraph_access_token:
            raise ValueError("Telegraph access token is not configured.")

        content = create_content_nodes(message)

        payload = {
            "access_token": settings.telegraph_access_token,
            "title": "Automated Social Media Update",
            "content": json.dumps(content),
            "return_content": "false",
        }

        url = "https://api.telegra.ph/createPage"

        try:
            logger.info("Creating a Telegraph page.")

            for attempt in range(3):
                try:
                    async with httpx.AsyncClient(
                        timeout=30.0,
                        trust_env=True,
                    ) as client:
                        response = await client.post(
                            url,
                            data=payload,
                        )

                    break

                except httpx.ConnectError:
                    if attempt == 2:
                        raise

                    logger.warning(
                        "Telegraph connection failed. " "Retrying (%s/2).",
                        attempt + 1,
                    )

                    await asyncio.sleep(attempt + 1)

            response.raise_for_status()
            result = response.json()

            if not result.get("ok"):
                raise RuntimeError(
                    result.get(
                        "error",
                        "Telegraph publishing failed.",
                    )
                )

            page = result["result"]
            page_path = page["path"]

            logger.info(
                "Telegraph page created successfully. " "Page path: %s",
                page_path,
            )

            return {
                "platform": self.platform_name,
                "status": "success",
                "page_path": page_path,
                "posted_url": page["url"],
                "public_access": True,
            }

        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
            RuntimeError,
        ):
            logger.exception("Telegraph publishing failed.")
            raise
