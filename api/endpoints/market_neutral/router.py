from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from api.deps.auth import authenticate_user
from api.schemas.completion_response import ChatCompletionResponse, CompletionRequest
from api.services.model_response import model_response

router = APIRouter(
    prefix="/v1/completions",
    tags=["completions"],
)


@router.post(
    "/",
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=ChatCompletionResponse,
)
def create_completion(
    completion_request: CompletionRequest,
):
    try:
        logger.info(f"Processing completion request: {completion_request}")
        conversation = model_response(completion_request.dict())
        logger.info(f"Completion processed successfully")
        return conversation
    except HTTPException as http_exc:
        logger.error(f"Failed to process completion: {http_exc}")
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to process completion", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process completion",
        )
