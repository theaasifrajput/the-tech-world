from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import (
    Course, Lesson, LessonTranslation, Module, ModuleTranslation,
)

router = APIRouter(prefix="/courses", tags=["curriculum"])


def _uuid_or_404(value: str) -> UUID:
    try:
        return UUID(value)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc


@router.get("/{course_id}/curriculum")
def get_course_curriculum(
    course_id: str,
    locale: str = Query(default="en", pattern="^(en|hi)$"),
    db: Session = Depends(get_db),
):
    parsed_id = _uuid_or_404(course_id)
    course = db.scalar(
        select(Course).where(Course.id == parsed_id, Course.status == "published")
    )
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    modules = db.execute(
        select(Module, ModuleTranslation)
        .join(ModuleTranslation, ModuleTranslation.module_id == Module.id)
        .where(Module.course_id == course.id, ModuleTranslation.locale == locale)
        .order_by(Module.position.asc())
    ).all()

    result_modules = []
    for module, module_translation in modules:
        lessons = db.execute(
            select(Lesson, LessonTranslation)
            .join(LessonTranslation, LessonTranslation.lesson_id == Lesson.id)
            .where(Lesson.module_id == module.id, LessonTranslation.locale == locale)
            .order_by(Lesson.position.asc())
        ).all()
        result_modules.append({
            "id": str(module.id),
            "position": module.position,
            "title": module_translation.title,
            "lessons": [
                {
                    "id": str(lesson.id),
                    "position": lesson.position,
                    "title": translation.title,
                    "description": translation.description,
                    "duration_seconds": lesson.duration_seconds,
                    "is_preview": lesson.is_preview,
                    # Do not disclose non-preview YouTube IDs before entitlement checks exist.
                    "youtube_video_id": lesson.youtube_video_id if lesson.is_preview else None,
                }
                for lesson, translation in lessons
            ],
        })
    return {"course_id": str(course.id), "locale": locale, "modules": result_modules}
