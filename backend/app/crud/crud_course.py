from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course, Module, Lesson
from app.schemas.course import CourseCreate, LessonCreate, ModuleCreate # Assuming these are defined

class CRUDCourse:
    def get_course(self, db: Session, course_id: int) -> Optional[Course]:
        return db.query(Course).options(
            joinedload(Course.modules).joinedload(Module.lessons)
        ).filter(Course.id == course_id).first()

    def get_course_by_slug(self, db: Session, slug: str) -> Optional[Course]:
        return db.query(Course).options(
            joinedload(Course.modules).joinedload(Module.lessons)
        ).filter(Course.slug == slug).first()

    def get_courses(
        self, db: Session, skip: int = 0, limit: int = 10, published_only: bool = True
    ) -> List[Course]:
        query = db.query(Course)
        if published_only:
            query = query.filter(Course.is_published == True)
        return query.offset(skip).limit(limit).all()

    def create_course(self, db: Session, *, obj_in: CourseCreate) -> Course:
        db_obj = Course(
            title=obj_in.title,
            description=obj_in.description,
            slug=obj_in.slug, # Consider auto-generating slug if not provided or to ensure uniqueness
            image_url=str(obj_in.image_url) if obj_in.image_url else None,
            is_published=obj_in.is_published,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Optional: Update course (can be added for Admin F1.6)
    # def update_course(self, db: Session, *, db_obj: Course, obj_in: CourseUpdate) -> Course:
    #     # Update fields
    #     ...
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

class CRUDModule:
    def get_module(self, db: Session, module_id: int) -> Optional[Module]:
        return db.query(Module).options(
            joinedload(Module.lessons)
        ).filter(Module.id == module_id).first()

    def create_module(self, db: Session, *, obj_in: ModuleCreate, course_id: int) -> Module:
        db_obj = Module(
            title=obj_in.title,
            description=obj_in.description,
            order=obj_in.order,
            course_id=course_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDLesson:
    def get_lesson(self, db: Session, lesson_id: int) -> Optional[Lesson]:
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def create_lesson(self, db: Session, *, obj_in: LessonCreate, module_id: int) -> Lesson:
        db_obj = Lesson(
            title=obj_in.title,
            content_type=obj_in.content_type,
            content_path=obj_in.content_path,
            content_text=obj_in.content_text, # Added content_text
            order=obj_in.order,
            module_id=module_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

course = CRUDCourse()
module = CRUDModule() # For potential use if needed separately
lesson = CRUDLesson() # For potential use if needed separately
