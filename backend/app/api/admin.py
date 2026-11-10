from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin
from app.models import (
    AdminAuditLog, Category, CategoryTranslation, Course, CourseTranslation,
    Lesson, LessonTranslation, Module, ModuleTranslation, User,
)
from app.schemas import CategoryCreate, CourseCreate, LessonCreate, ModuleCreate

router = APIRouter(prefix="/admin", tags=["admin"])


def _parse_uuid(value: str, entity: str) -> UUID:
    try:
        return UUID(value)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=f"{entity} not found") from exc


def _audit(db: Session, admin: User, action: str, entity_type: str, entity_id: UUID):
    db.add(AdminAuditLog(
        admin_user_id=admin.id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
    ))


def _flush(db: Session):
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A record with a conflicting slug or position already exists") from exc


def _commit(db: Session):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="A record with a conflicting slug or position already exists") from exc


@router.get("/me")
def admin_me(admin: User = Depends(require_admin)):
    return {"id": str(admin.id), "email": admin.email, "role": admin.role}


@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    category = Category(slug=payload.slug)
    db.add(category)
    _flush(db)
    db.add(CategoryTranslation(category_id=category.id, locale="en", name=payload.name_en, description=payload.description_en))
    if payload.name_hi:
        db.add(CategoryTranslation(category_id=category.id, locale="hi", name=payload.name_hi, description=payload.description_hi))
    _audit(db, admin, "category.create", "category", category.id)
    _commit(db)
    return {"id": str(category.id), "slug": category.slug}


@router.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    category_id = None
    if payload.category_id:
        category_id = _parse_uuid(payload.category_id, "Category")
        if db.get(Category, category_id) is None:
            raise HTTPException(status_code=404, detail="Category not found")
    course = Course(
        category_id=category_id, slug=payload.slug, thumbnail_url=payload.thumbnail_url,
        level=payload.level, is_free=payload.is_free, status="draft",
    )
    db.add(course)
    _flush(db)
    db.add(CourseTranslation(course_id=course.id, locale="en", title=payload.title_en, description=payload.description_en))
    if payload.title_hi:
        db.add(CourseTranslation(course_id=course.id, locale="hi", title=payload.title_hi, description=payload.description_hi))
    _audit(db, admin, "course.create", "course", course.id)
    _commit(db)
    return {"id": str(course.id), "slug": course.slug, "status": course.status}


@router.post("/courses/{course_id}/modules", status_code=status.HTTP_201_CREATED)
def create_module(
    course_id: str,
    payload: ModuleCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    parsed_id = _parse_uuid(course_id, "Course")
    if db.get(Course, parsed_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    module = Module(course_id=parsed_id, position=payload.position)
    db.add(module)
    _flush(db)
    db.add(ModuleTranslation(module_id=module.id, locale="en", title=payload.title_en))
    if payload.title_hi:
        db.add(ModuleTranslation(module_id=module.id, locale="hi", title=payload.title_hi))
    _audit(db, admin, "module.create", "module", module.id)
    _commit(db)
    return {"id": str(module.id), "position": module.position}


@router.post("/modules/{module_id}/lessons", status_code=status.HTTP_201_CREATED)
def create_lesson(
    module_id: str,
    payload: LessonCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    parsed_id = _parse_uuid(module_id, "Module")
    if db.get(Module, parsed_id) is None:
        raise HTTPException(status_code=404, detail="Module not found")
    lesson = Lesson(
        module_id=parsed_id, position=payload.position,
        youtube_video_id=payload.youtube_video_id,
        duration_seconds=payload.duration_seconds, is_preview=payload.is_preview,
    )
    db.add(lesson)
    _flush(db)
    db.add(LessonTranslation(
        lesson_id=lesson.id, locale="en", title=payload.title_en,
        description=payload.description_en,
    ))
    if payload.title_hi:
        db.add(LessonTranslation(
            lesson_id=lesson.id, locale="hi", title=payload.title_hi,
            description=payload.description_hi,
        ))
    _audit(db, admin, "lesson.create", "lesson", lesson.id)
    _commit(db)
    return {"id": str(lesson.id), "position": lesson.position, "is_preview": lesson.is_preview}


@router.post("/courses/{course_id}/publish")
def publish_course(
    course_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    parsed_id = _parse_uuid(course_id, "Course")
    course = db.get(Course, parsed_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    has_english_title = db.scalar(select(CourseTranslation.id).where(
        CourseTranslation.course_id == course.id, CourseTranslation.locale == "en"
    ))
    if not has_english_title:
        raise HTTPException(status_code=422, detail="An English course title is required before publishing")
    course.status = "published"
    _audit(db, admin, "course.publish", "course", course.id)
    _commit(db)
    return {"id": str(course.id), "status": course.status}
