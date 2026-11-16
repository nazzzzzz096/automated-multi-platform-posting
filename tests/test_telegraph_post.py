
import asyncio

from app.platforms.telegraph import post_to_telegraph


async def main():
    """Test publishing a Telegraph page."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    result = await post_to_telegraph(message)

    print("Telegraph publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
