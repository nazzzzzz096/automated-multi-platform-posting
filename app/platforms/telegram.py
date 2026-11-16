import logging

import httpx

from app.config import settings
from app.platforms.base import BasePlatform

logger = logging.getLogger(__name__)


class TelegramPlatform(BasePlatform):
    """Publish messages to Telegram."""

    platform_name = "telegram"

    async def publish(self, message: str) -> dict:
        """Publish a message using the Telegram Bot API."""

        if not settings.telegram_bot_token:
            raise ValueError("Telegram bot token is not configured.")

        if not settings.telegram_chat_id:
            raise ValueError("Telegram chat ID is not configured.")

        api_url = (
            "https://api.telegram.org/bot" f"{settings.telegram_bot_token}/sendMessage"
        )

        payload = {
            "chat_id": settings.telegram_chat_id,
            "text": message,
        }

        try:
            logger.info("Publishing message to Telegram.")

            async with httpx.AsyncClient(
                timeout=20.0,
                trust_env=True,
            ) as client:
                response = await client.post(
                    api_url,
                    json=payload,
                )

                response.raise_for_status()
                result = response.json()

            if not result.get("ok"):
                raise RuntimeError(
                    result.get(
                        "description",
                        "Telegram message publishing failed.",
                    )
                )

            posted_message = result["result"]
            message_id = posted_message["message_id"]

            chat = posted_message["chat"]
            username = chat.get("username")
            chat_type = chat.get("type")

            posted_url = None

            if username and chat_type in (
                "channel",
                "supergroup",
            ):
                posted_url = f"https://t.me/{username}/{message_id}"

            logger.info(
                "Telegram message published successfully. " "Message ID: %s",
                message_id,
            )

            return {
                "platform": self.platform_name,
                "status": "success",
                "message_id": message_id,
                "posted_url": posted_url,
                "public_access": bool(posted_url),
            }

        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
            RuntimeError,
        ):
            logger.exception("Telegram publishing failed.")
            raise
