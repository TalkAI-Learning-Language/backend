import uuid

from requests import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
from typing_extensions import Any

from app.api.deps import SessionDep
from app.model.lesson import LessonCreate, Lesson, LessonsPublic

router = APIRouter(prefix="/progress", tags=["progress"])

