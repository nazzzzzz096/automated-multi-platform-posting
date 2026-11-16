import asyncio

from app.platforms.telegraph import TelegraphPlatform


async def main():
    """Test publishing a Telegraph page."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    platform = TelegraphPlatform()
    result = await platform.publish(message)

    print("Telegraph publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
