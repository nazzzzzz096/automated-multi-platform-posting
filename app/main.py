from fastapi import FastAPI

from app.schemas import PostingRequest
from app.services.llm_service import improve_message

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description=(
        "An API for publishing messages across "
        "multiple platforms."
    ),
    version="1.0.0",
)


@app.get("/")
async def home():
    """Check whether the API is running."""

    return {
        "success": True,
        "message": "Automated Posting API is running.",
    }

@app.post("/posting")
async def create_post(request: PostingRequest):
    """Validate and improve the submitted message."""

    original_message = request.message

    improved_message = await improve_message(
        original_message
    )

    return {
        "success": True,
        "status": "processed",
        "message": "Message validated and improved successfully.",
        "original_message": original_message,
        "improved_message": improved_message,
        "character_count": len(improved_message),
        "publishing_status": "Not published yet",
    }