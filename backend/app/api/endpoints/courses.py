from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas # Use this to access schemas via schemas.Course, etc.
from app.crud.crud_course import course as course_crud # Use the instance
from app.db.session import get_db
# from app.core.security import get_current_active_user # For protected endpoints if needed later

router = APIRouter()

@router.get("/", response_model=List[schemas.course.CourseSummary])
def read_courses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), # Max 100 courses per page
    published_only: bool = Query(True) # Default to only showing published courses
):
    """
    Retrieve a list of courses.
    - Use `published_only=false` to see unpublished courses (e.g., for admins or previews).
    """
    courses = course_crud.get_courses(db, skip=skip, limit=limit, published_only=published_only)
    return courses

@router.get("/{slug}", response_model=schemas.course.Course) # Returns full course details
def read_course_by_slug(
    slug: str,
    db: Session = Depends(get_db)
    # current_user: Optional[schemas.user.User] = Depends(get_current_active_user_optional) # Example for conditional access
):
    """
    Get a specific course by its slug.
    Returns full course details including modules and lessons.
    """
    db_course = course_crud.get_course_by_slug(db, slug=slug)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # Example: Check if course is published or if user has rights (simplified here)
    # if not db_course.is_published and (not current_user or not current_user.is_superuser):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this course.")

    return db_course


# Placeholder for course creation - typically an admin-only operation
# For F1.6 Admin - Course Management
# @router.post("/", response_model=schemas.course.Course, status_code=status.HTTP_201_CREATED)
# def create_new_course(
#     *,
#     db: Session = Depends(get_db),
#     course_in: schemas.course.CourseCreate,
#     # current_user: models.User = Depends(get_current_active_superuser) # Protect this endpoint
# ):
#     """
#     Create a new course. (Admin only)
#     """
#     # Basic check for slug uniqueness if not handled by DB constraint robustly or if pre-checking
#     existing_course = course_crud.get_course_by_slug(db, slug=course_in.slug)
#     if existing_course:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Course with slug '{course_in.slug}' already exists.",
#         )
#     course = course_crud.create_course(db=db, obj_in=course_in)
#     return course
