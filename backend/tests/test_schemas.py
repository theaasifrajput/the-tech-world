import pytest
from pydantic import ValidationError

from app.schemas import CategoryCreate, CourseCreate, LessonCreate, ModuleCreate


def test_category_slug_must_be_url_friendly():
    assert CategoryCreate(slug="machine-learning", name_en="Machine Learning").slug == "machine-learning"
    with pytest.raises(ValidationError):
        CategoryCreate(slug="Machine Learning", name_en="Machine Learning")


def test_course_requires_english_title():
    with pytest.raises(ValidationError):
        CourseCreate(slug="python-basics")


def test_module_position_must_be_positive():
    with pytest.raises(ValidationError):
        ModuleCreate(position=0, title_en="Introduction")


def test_lesson_duration_must_be_positive():
    with pytest.raises(ValidationError):
        LessonCreate(position=1, title_en="Intro", duration_seconds=0)
