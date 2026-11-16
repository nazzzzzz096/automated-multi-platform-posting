
import logging
import re

from google import genai
from google.genai import types

from app.config import settings


logger = logging.getLogger(__name__)


def extract_urls(message: str) -> list[str]:
    """Extract URLs while removing common trailing punctuation."""

    urls = re.findall(r"https?://[^\s<>]+", message)

    return [
        url.rstrip(".,!?;:)")
        for url in urls
    ]


async def improve_message(message: str) -> str:
    """
    Improve grammar and readability without changing the
    original meaning or URL.

    Return the original message if Gemini produces an
    invalid response or the API request fails.
    """

    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    original_urls = extract_urls(message)

    prompt = f"""
You are a professional proofreader.

Correct spelling and grammar in the message below.
Make only small improvements to readability.

STRICT RULES:
1. Preserve the original meaning and context.
2. Do not add new facts, claims, or promises.
3. Do not remove important information.
4. Preserve the original tone.
5. Keep every URL exactly unchanged.
6. Do not add another URL.
7. Return only the corrected message.
8. Keep the result within 200 characters.

Original message:
{message}
"""

    try:
        async with genai.Client(
            api_key=settings.gemini_api_key
        ).aio as client:
            response = await client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=256,
                ),
            )

        improved_message = (response.text or "").strip()

        improved_urls = extract_urls(improved_message)

        if (
            not improved_message
            or len(improved_message) > 200
            or improved_urls != original_urls
        ):
            logger.warning(
                "Gemini returned an invalid message. "
                "Using the original message."
            )
            return message

        return improved_message

    except Exception:
        logger.exception(
            "Gemini request failed. Using the original message."
        )
        return message
