from typing import Optional
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


router = APIRouter()

task_list = []

class Status (str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status : Optional[Status] = Status.todo
    priority : Optional[Priority] = Priority.low
    tags : Optional[list[str]] = None
    created_at :Optional[datetime]= None


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task:Task):
    task.created_at = datetime.now()
    task_list.append(task)
    return task_list