
import asyncio

import httpx

from app.config import settings


async def main():
    """Inspect pending Telegram updates."""

    token = settings.telegram_bot_token

    if not token:
        print("Telegram token is missing.")
        return

    url = f"https://api.telegram.org/bot{token}/getUpdates"

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    print("Telegram API success:", data.get("ok"))

    for update in data.get("result", []):
        print("\nUpdate ID:", update.get("update_id"))
        print("Update types:", list(update.keys()))

        for update_type in (
            "message",
            "edited_message",
            "channel_post",
            "my_chat_member",
        ):
            item = update.get(update_type)

            if item:
                chat = item.get("chat", {})

                print("Chat ID:", chat.get("id"))
                print("Chat type:", chat.get("type"))
                print("Chat username:", chat.get("username"))
                print("Message text:", item.get("text"))
                break


if __name__ == "__main__":
    asyncio.run(main())
