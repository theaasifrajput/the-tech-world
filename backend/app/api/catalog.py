from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Course, CourseTranslation

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("")
def list_courses(
    locale: str = Query(default="en", pattern="^(en|hi)$"),
    category: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    statement = (
        select(Course, CourseTranslation)
        .join(CourseTranslation, CourseTranslation.course_id == Course.id)
        .where(Course.status == "published", CourseTranslation.locale == locale)
        .order_by(Course.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if category:
        try:
            category_id = UUID(category)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="category must be a valid UUID") from exc
        statement = statement.where(Course.category_id == category_id)
    rows = db.execute(statement).all()
    return {
        "items": [
            {
                "id": str(course.id),
                "slug": course.slug,
                "title": translation.title,
                "description": translation.description,
                "thumbnail_url": course.thumbnail_url,
                "level": course.level,
                "is_free": course.is_free,
            }
            for course, translation in rows
        ],
        "locale": locale,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{course_id}")
def get_course(course_id: str, locale: str = Query(default="en", pattern="^(en|hi)$"), db: Session = Depends(get_db)):
    from uuid import UUID
    try:
        parsed_id = UUID(course_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc
    row = db.execute(
        select(Course, CourseTranslation)
        .join(CourseTranslation, CourseTranslation.course_id == Course.id)
        .where(Course.id == parsed_id, Course.status == "published", CourseTranslation.locale == locale)
    ).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course, translation = row
    return {
        "id": str(course.id), "slug": course.slug, "title": translation.title,
        "description": translation.description, "thumbnail_url": course.thumbnail_url,
        "level": course.level, "is_free": course.is_free,
    }
