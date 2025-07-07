import uuid

from requests import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
from typing_extensions import Any

from app.api.deps import SessionDep
from app.model.lesson import LessonCreate, Lesson, LessonsPublic

router = APIRouter(prefix="/lessons", tags=["lessons"])



def create_lesson(*, session: Session, item_in: LessonCreate, owner_id: uuid.UUID) -> Lesson:
    db_lesson = Lesson.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_lesson)
    session.commit()
    session.refresh(db_lesson)
    return db_lesson


@router.get("/", response_model=LessonsPublic)
def get_lessons(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
        """
        Retrieve Lessons
        """

        count_statement = select(func.count()).select_from(Lesson)
        count = session.exec(count_statement)

        statement = select(Lesson).offset(skip).limit(limit)
        lessons = session.exec(statement).all()

        return LessonsPublic(data=lessons, count=count)