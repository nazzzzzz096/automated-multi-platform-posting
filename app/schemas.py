import re

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    TypeAdapter,
    field_validator,
)


class PostingRequest(BaseModel):
    """Validate the message submitted for multi-platform posting."""

    message: str = Field(
        min_length=1,
        max_length=200,
        description="Message containing exactly one valid URL.",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        """Ensure the message contains exactly one valid URL."""

        urls = re.findall(r"https?://[^\s<>]+", value)
        urls = [url.rstrip(".,!?;:)") for url in urls]

        if len(urls) != 1:
            raise ValueError("Message must contain exactly one URL.")

        try:
            TypeAdapter(HttpUrl).validate_python(urls[0])
        except ValueError as exc:
            raise ValueError("The URL provided is invalid.") from exc

        return value
