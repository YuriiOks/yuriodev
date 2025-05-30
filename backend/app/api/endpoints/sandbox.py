from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from app.services.code_runner import run_python_code
from app.core.security import get_current_active_user # To protect the endpoint
from app.models.user import User as DBUser # For type hinting current_user

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str = Field(..., max_length=10000) # Max 10k characters for code
    language: Optional[str] = "python" # Default to python, extendable later

class CodeExecutionResponse(BaseModel):
    output: str
    error: str
    execution_time: float
    success: bool
    exit_code: Optional[int] = None


@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code_endpoint(
    payload: CodeExecutionRequest,
    current_user: DBUser = Depends(get_current_active_user) # Protect endpoint
):
    """
    Execute user-submitted code in a sandboxed environment.
    Currently supports Python.
    """
    if payload.language.lower() != "python":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{payload.language}' is not supported. Only Python is currently available."
        )

    if not payload.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No code provided for execution."
        )

    # Add rate limiting here in a real application to prevent abuse

    try:
        result = run_python_code(payload.code)
        return result
    except Exception as e:
        # This is a fallback, run_python_code should handle its own errors.
        # Log this unexpected error.
        # logger.error(f"Unexpected error in /execute endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while trying to execute code."
        )
