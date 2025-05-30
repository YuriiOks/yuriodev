from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.models.course import LessonContentType # Import the Enum

# Lesson Schemas
class LessonBase(BaseModel):
    title: str
    content_type: LessonContentType
    content_path: Optional[str] = None
    content_text: Optional[str] = None # Added content_text
    order: int = 0

class LessonCreate(LessonBase):
    module_id: int # Required for creation context, but might not be in Lesson model directly for updates if lesson moves

class Lesson(LessonBase):
    id: int
    module_id: int # Keep module_id for context
    # content_text is inherited from LessonBase and will be included
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # from_attributes = True # For Pydantic V2

# Module Schemas
class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0

class ModuleCreate(ModuleBase):
    course_id: int # Required for creation context

class Module(ModuleBase):
    id: int
    course_id: int # Keep course_id for context
    lessons: List[Lesson] = [] # Nested list of Lesson schemas
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    slug: str # Slugs should be carefully managed, perhaps auto-generated from title
    image_url: Optional[HttpUrl] = None # Validate as URL
    is_published: bool = False

class CourseCreate(CourseBase):
    pass # All fields from CourseBase are needed for creation

# For returning a list of courses (catalog view) - less detail
class CourseSummary(CourseBase):
    id: int
    created_at: datetime # Optional: might not be needed for summary
    updated_at: datetime # Optional: might not be needed for summary
    # Potentially add number of modules or estimated duration later

    class Config:
        orm_mode = True
        # from_attributes = True

# For returning a single course with all details
class Course(CourseBase):
    id: int
    modules: List[Module] = [] # Nested list of Module schemas
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # from_attributes = True
