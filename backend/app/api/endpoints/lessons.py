from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas # To access schemas.lesson.Lesson
from app.crud.crud_course import lesson as lesson_crud # Using the lesson CRUD instance
from app.db.session import get_db
# from app.models.user import User as DBUser # For auth if needed
# from app.core.security import get_current_active_user # For auth if needed

router = APIRouter()

@router.get("/{lesson_id}", response_model=schemas.course.Lesson) # Use schemas.course.Lesson
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    # current_user: Optional[DBUser] = Depends(get_current_active_user_optional) # Example for optional auth
):
    """
    Retrieve a single lesson by its ID.
    Content (e.g., text, video URL) is included.
    """
    db_lesson = lesson_crud.get_lesson(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    # Add any authorization logic here if lessons are not publicly accessible
    # For F1.3, assume public if course is published (handled at course level for now)

    return db_lesson
