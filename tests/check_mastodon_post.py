import asyncio

from app.platforms.mastodon import post_to_mastodon


async def main():
    """Test publishing a message to Mastodon."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    result = await post_to_mastodon(message)

    print("Mastodon publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
