from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base

# Enum for Lesson Content Type
class LessonContentType(enum.Enum):
    TEXT = "text"
    VIDEO = "video"
    QUIZ = "quiz"
    CODE_SANDBOX = "code_sandbox"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=True)
    is_published = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(title='{self.title}', slug='{self.slug}')>"

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0) # Order within the course

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order") # Ensure lessons are ordered

    def __repr__(self):
        return f"<Module(title='{self.title}', course_id={self.course_id})>"

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    content_type = Column(SAEnum(LessonContentType, name="lessoncontenttype"), nullable=False)
    # content_path could be:
    # - For TEXT: path to a Markdown file, or direct content if small (not recommended for large text)
    # - For VIDEO: Video ID (e.g., YouTube, Vimeo) or path to video file
    # - For QUIZ: ID of a quiz object (if quizzes are stored separately) or JSON structure
    # - For CODE_SANDBOX: Configuration ID or path to setup files
    content_path = Column(String, nullable=True) # For non-text content like video IDs, external links etc.
    content_text = Column(Text, nullable=True) # For storing TEXT type content (e.g. Markdown) directly

    order = Column(Integer, nullable=False, default=0) # Order within the module

    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    module = relationship("Module", back_populates="lessons")

    def __repr__(self):
        return f"<Lesson(title='{self.title}', module_id={self.module_id}, type='{self.content_type.value}')>"
