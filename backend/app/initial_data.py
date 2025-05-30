import logging
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.crud.crud_course import course as course_crud, module as module_crud, lesson as lesson_crud
from app.schemas.course import CourseCreate, ModuleCreate, LessonCreate
from app.models.course import LessonContentType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COURSE_PYTHON_FOR_DL = {
    "title": "Python for Deep Learning Essentials",
    "slug": "python-for-dl-essentials",
    "description": "A quick tour of essential Python features and libraries commonly used in deep learning projects.",
    "image_url": "https://example.com/images/python_dl.jpg", # Replace with a real or placeholder URL
    "is_published": True,
    "modules": [
        {
            "title": "Core Python Refresher",
            "order": 1,
            "lessons": [
                {
                    "title": "Data Structures (Lists, Dicts, Sets, Tuples)",
                    "order": 1,
                    "content_type": LessonContentType.TEXT,
                    "content_text": """## Python Data Structures

Understanding Python's built-in data structures is crucial.

### Lists
Ordered, mutable sequences.
`my_list = [1, "hello", 3.14]`

### Dictionaries
Unordered (in older Python versions) key-value pairs.
`my_dict = {"name": "Yuri", "skill": "AI"}`

### Sets
Unordered collections of unique elements.
`my_set = {1, 2, 2, 3}` (results in `{1, 2, 3}`)

### Tuples
Ordered, immutable sequences.
`my_tuple = (1, "immutable", True)`
"""
                },
                {
                    "title": "Functions and Lambdas",
                    "order": 2,
                    "content_type": LessonContentType.TEXT,
                    "content_text": """## Functions and Lambdas in Python

Functions are blocks of reusable code.

```python
def greet(name):
    return f"Hello, {name}!"
```

Lambda functions are small, anonymous functions:
`square = lambda x: x * x`
`print(square(5)) # Output: 25`
"""
                }
            ]
        },
        {
            "title": "Introduction to NumPy",
            "order": 2,
            "lessons": [
                {
                    "title": "NumPy Arrays",
                    "order": 1,
                    "content_type": LessonContentType.TEXT,
                    "content_text": """## NumPy Arrays

NumPy's core feature is the n-dimensional array (ndarray).
It's fast and memory efficient.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)
print(arr.dtype)
```
"""
                }
            ]
        }
    ]
}

COURSE_GIT_ESSENTIALS = {
    "title": "Git Essentials for Developers",
    "slug": "git-essentials",
    "description": "Learn the fundamental Git commands and workflows to manage your code effectively.",
    "image_url": "https://example.com/images/git_essentials.jpg", # Replace
    "is_published": True,
    "modules": [
        {
            "title": "Getting Started with Git",
            "order": 1,
            "lessons": [
                {
                    "title": "What is Version Control?",
                    "order": 1,
                    "content_type": LessonContentType.TEXT,
                    "content_text": """## What is Version Control?

Version control systems (VCS) track changes to files over time.
Git is a distributed VCS.
Key benefits: history, branching, collaboration.
"""
                },
                {
                    "title": "Basic Git Commands",
                    "order": 2,
                    "content_type": LessonContentType.TEXT,
                    "content_text": """## Basic Git Commands

*   `git init`: Initialize a new Git repository.
*   `git clone <url>`: Copy a remote repository.
*   `git add <file>`: Stage changes.
*   `git commit -m "message"`: Commit staged changes.
*   `git status`: Show current status.
*   `git log`: View commit history.
"""
                }
            ]
        }
    ]
}

COURSES_DATA = [COURSE_PYTHON_FOR_DL, COURSE_GIT_ESSENTIALS]

def populate_initial_data(db: Session) -> None:
    logger.info("Starting initial data population...")

    for course_data in COURSES_DATA:
        course = course_crud.get_course_by_slug(db, slug=course_data["slug"])
        if not course:
            logger.info(f"Creating course: {course_data['title']}")
            course_in = CourseCreate(
                title=course_data["title"],
                description=course_data["description"],
                slug=course_data["slug"],
                image_url=course_data.get("image_url"),
                is_published=course_data["is_published"]
            )
            course = course_crud.create_course(db=db, obj_in=course_in)
        else:
            logger.info(f"Course already exists: {course_data['title']}")

        for module_data in course_data["modules"]:
            # Check if module exists by title and course_id (more robust check needed if titles aren't unique per course)
            # For simplicity, we assume if course exists, we don't re-add modules/lessons this way.
            # A more robust system would check module by title/order under this course.
            # If course was just created, its modules won't exist.

            # Let's check if module exists for this course
            module_exists = any(mod.title == module_data["title"] for mod in course.modules)

            if not module_exists:
                logger.info(f"Creating module: {module_data['title']} for course {course.title}")
                module_in = ModuleCreate(
                    title=module_data["title"],
                    description=module_data.get("description"),
                    order=module_data["order"]
                    # course_id is passed directly to crud function
                )
                module = module_crud.create_module(db=db, obj_in=module_in, course_id=course.id)

                for lesson_data in module_data["lessons"]:
                    logger.info(f"Creating lesson: {lesson_data['title']} for module {module.title}")
                    lesson_in = LessonCreate(
                        title=lesson_data["title"],
                        content_type=lesson_data["content_type"],
                        content_text=lesson_data.get("content_text"),
                        content_path=lesson_data.get("content_path"),
                        order=lesson_data["order"]
                        # module_id is passed directly to crud function
                    )
                    lesson_crud.create_lesson(db=db, obj_in=lesson_in, module_id=module.id)
            else:
                 logger.info(f"Module {module_data['title']} (or course) already processed for lessons.")


    logger.info("Initial data population finished.")

if __name__ == "__main__":
    logger.info("Creating initial data from script execution...")
    db = SessionLocal()
    try:
        populate_initial_data(db)
    finally:
        db.close()
    logger.info("Initial data script finished.")
