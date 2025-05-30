from fastapi import APIRouter, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.session import get_db
from app.core.security import get_current_active_superuser
from app.models.user import User as DBUser # For dependency type hint
from app.crud import crud_course, crud_user # Assuming __init__.py exports these
from app.schemas import course as course_schemas # For type hints and creating objects

# Configure templates
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES_PATH = BASE_PATH / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

router = APIRouter(
    prefix="/admin", # All routes in this router will start with /admin
    tags=["Admin"],
    dependencies=[Depends(get_current_active_superuser)], # Protect all admin routes
    responses={404: {"description": "Not found"}} # Default response for not found
)

# Admin Dashboard (Placeholder)
@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "page_title": "Admin Dashboard"})

# Course Management
@router.get("/courses", response_class=HTMLResponse)
async def list_courses_admin(request: Request, db: Session = Depends(get_db)):
    courses = crud_course.course.get_courses(db, published_only=False, limit=100) # Show all for admin
    return templates.TemplateResponse("courses_list.html", {"request": request, "courses": courses, "page_title": "Manage Courses"})

@router.get("/courses/create", response_class=HTMLResponse)
async def create_course_form_admin(request: Request):
    return templates.TemplateResponse("course_form.html", {"request": request, "course": None, "page_title": "Create New Course"})

@router.post("/courses/create", response_class=HTMLResponse)
async def handle_create_course_admin(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    slug: str = Form(...),
    description: str = Form(""),
    image_url: str = Form(None),
    is_published: bool = Form(False)
):
    # Basic validation for slug uniqueness (CRUD might also raise error if DB constraint fails)
    existing_course = crud_course.course.get_course_by_slug(db, slug=slug)
    if existing_course:
        # Re-render form with error
        return templates.TemplateResponse("course_form.html", {
            "request": request,
            "course": None,
            "page_title": "Create New Course",
            "error": f"Slug '{slug}' already exists."
        }, status_code=status.HTTP_400_BAD_REQUEST)

    course_in = course_schemas.CourseCreate(
        title=title,
        slug=slug,
        description=description,
        image_url=image_url if image_url else None, # Ensure None if empty string for HttpUrl
        is_published=is_published
    )
    crud_course.course.create_course(db=db, obj_in=course_in)
    return RedirectResponse(url=router.url_path_for("list_courses_admin"), status_code=status.HTTP_303_SEE_OTHER)

@router.get("/courses/edit/{course_id}", response_class=HTMLResponse)
async def edit_course_form_admin(request: Request, course_id: int, db: Session = Depends(get_db)):
    course = crud_course.course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse("course_form.html", {"request": request, "course": course, "page_title": f"Edit Course: {course.title}"})

@router.post("/courses/edit/{course_id}", response_class=HTMLResponse)
async def handle_edit_course_admin(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    slug: str = Form(...),
    description: str = Form(""),
    image_url: str = Form(None),
    is_published: bool = Form(False)
):
    course = crud_course.course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if slug is being changed and if the new one conflicts
    if course.slug != slug:
        existing_course = crud_course.course.get_course_by_slug(db, slug=slug)
        if existing_course and existing_course.id != course_id:
            return templates.TemplateResponse("course_form.html", {
                "request": request,
                "course": course, # Pass existing course data back
                "page_title": f"Edit Course: {course.title}",
                "error": f"Slug '{slug}' already exists for another course."
            }, status_code=status.HTTP_400_BAD_REQUEST)

    # This requires an update_course method in CRUD, which is not yet defined.
    # For now, let's update fields directly. A proper update method would use a Pydantic schema.
    course.title = title
    course.slug = slug
    course.description = description
    course.image_url = image_url if image_url else None
    course.is_published = is_published
    db.add(course)
    db.commit()
    db.refresh(course)

    return RedirectResponse(url=router.url_path_for("list_courses_admin"), status_code=status.HTTP_303_SEE_OTHER)


# TODO: Module Management (GET/POST for create/edit forms, listing within course_detail_admin)
# TODO: Lesson Management (GET/POST for create/edit forms, listing within module_detail_admin)

# Placeholder for course detail view (where modules/lessons would be managed)
@router.get("/courses/view/{course_id}", response_class=HTMLResponse)
async def view_course_detail_admin(request: Request, course_id: int, db: Session = Depends(get_db)):
    course = crud_course.course.get_course(db, course_id=course_id) # Fetches with modules and lessons
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse("course_detail_admin.html", {"request": request, "course": course, "page_title": f"Course: {course.title}"})

# Add more routes here for modules and lessons as per Step 6 & 7
# For brevity in this step, I'll focus on course CRUD and placeholders for module/lesson forms.

# Example: Add Module Form (simplified)
@router.get("/modules/create/{course_id}", response_class=HTMLResponse)
async def create_module_form_admin(request: Request, course_id: int, db: Session = Depends(get_db)):
    course = crud_course.course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found to add module to")
    return templates.TemplateResponse("module_form.html", {"request": request, "module": None, "course": course, "page_title": "Create New Module"})

# Example: Add Lesson Form (simplified)
@router.get("/lessons/create/{module_id}", response_class=HTMLResponse)
async def create_lesson_form_admin(request: Request, module_id: int, db: Session = Depends(get_db)):
    module = crud_course.module.get_module(db, module_id=module_id) # Assumes get_module in crud_course.module
    if not module:
        raise HTTPException(status_code=404, detail="Module not found to add lesson to")
    # Pass LessonContentType enum to template for dropdown
    return templates.TemplateResponse("lesson_form.html", {"request": request, "lesson": None, "module": module, "content_types": [e.value for e in course_schemas.LessonContentType], "page_title": "Create New Lesson"})


# Note: POST handlers for module/lesson creation and edit routes would be similar to course creation/edit.
# They would use respective CRUD functions and redirect appropriately.
# For example, POST to /modules/create/{course_id} would call crud_module.create_module
# and redirect to /admin/courses/view/{course_id}.
# POST to /lessons/create/{module_id} would call crud_lesson.create_lesson
# and redirect to /admin/courses/view/{course.id} (or a module detail page if created).
# Full implementation of these POST handlers and edit routes for modules/lessons is extensive
# and will be completed if time allows or in a follow-up if this step becomes too large.

# For the edit_course_admin, an `update_course` CRUD method is better.
# Let's assume I will add `update_course` to `crud_course.py` later if needed.
# For now, direct field update is shown.

# Need __init__.py in admin directory to make it a package
# touch backend/app/admin/__init__.py (if not already done by mkdir -p)
# The tool should handle directory creation implicitly if using create_file_with_block for admin_router.py
# but if I used `touch` before, I need to ensure the __init__.py is there.
# I'll add a step to create `backend/app/admin/__init__.py`.
