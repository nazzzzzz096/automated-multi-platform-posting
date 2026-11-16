
import httpx

from app.config import settings


async def post_to_telegram(message: str) -> dict:
    """Publish a message to Telegram using the Bot API."""

    if not settings.telegram_bot_token:
        raise ValueError(
            "Telegram bot token is not configured."
        )

    if not settings.telegram_chat_id:
        raise ValueError(
            "Telegram chat ID is not configured."
        )

    api_url = (
        "https://api.telegram.org/bot"
        f"{settings.telegram_bot_token}/sendMessage"
    )

    payload = {
        "chat_id": settings.telegram_chat_id,
        "text": message,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
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

    if username and chat_type in ("channel", "supergroup"):
        posted_url = (
        f"https://t.me/{username}/{message_id}"
        )

    return {
        "platform": "telegram",
        "status": "success",
        "message_id": message_id,
        "posted_url": posted_url,
    }
