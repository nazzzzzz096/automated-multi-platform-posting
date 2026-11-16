import asyncio

from app.platforms.devto import post_to_devto


async def main():
    """Test creating a DEV.to draft article."""

    message = (
        "Hello! This is a test from my Python "
        "multi-platform posting system. "
        "https://example.com"
    )

    result = await post_to_devto(message)

    print("DEV.to publishing result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
