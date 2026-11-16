import asyncio

from app.platforms.telegram import post_to_telegram


async def main():
    """Test publishing a message to Telegram."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    result = await post_to_telegram(message)

    print("Telegram publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
