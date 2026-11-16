
import asyncio

from app.platforms.bluesky import post_to_bluesky


async def main():
    """Test publishing a post to Bluesky."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    result = await post_to_bluesky(message)

    print("Bluesky publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
