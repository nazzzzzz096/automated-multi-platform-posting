from fastapi import FastAPI

from app.schemas import PostingRequest
from app.services.llm_service import improve_message
from app.services.posting_service import (
    publish_to_all_platforms,
)

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description=("An API for publishing messages across " "multiple platforms."),
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
    """Validate, improve and publish a message."""

    original_message = request.message

    improved_message = await improve_message(original_message)

    results = await publish_to_all_platforms(improved_message)

    successful_count = sum(result["status"] == "success" for result in results)

    failed_count = len(results) - successful_count

    if failed_count == 0:
        publishing_status = "success"
    elif successful_count > 0:
        publishing_status = "partial_success"
    else:
        publishing_status = "failed"

    return {
        "success": failed_count == 0,
        "publishing_status": publishing_status,
        "message": "Publishing process completed.",
        "original_message": original_message,
        "improved_message": improved_message,
        "character_count": len(improved_message),
        "total_platforms": len(results),
        "successful_platforms": successful_count,
        "failed_platforms": failed_count,
        "results": results,
    }
