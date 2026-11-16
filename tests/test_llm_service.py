
import asyncio

from app.services.llm_service import improve_message


async def main():
    original_message = (
        "We provides best service for your business "
        "visit https://example.com"
    )

    improved_message = await improve_message(
        original_message
    )

    print("Original message:")
    print(original_message)

    print("\nImproved message:")
    print(improved_message)

    print("\nCharacter count:")
    print(len(improved_message))


if __name__ == "__main__":
    asyncio.run(main())
