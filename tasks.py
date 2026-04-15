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

@router.get("/tasks/", status_code=status.HTTP_200_OK)
async def get_tasks(keyword: str | None = None, status : str | None = None, priority : str | None = None, tag : str | None = None):
    results = []
    if keyword :
        for task in task_list:
            if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower():
                results.append(task)
        return results
    if status :
        for task in task_list:
            if status.lower() in task.status.lower():
                results.append(task)
        return results
    if priority :
        for task in task_list:
            if priority.lower() in task.priority.lower():
                results.append(task)
        return results
    if tag:
        for task in task_list:
            if any(tag.lower() in t.lower() for t in task.tags or [] ) :
                results.append(task)
        return results
    return task_list

@router.get("/tasks/{id}", status_code=status.HTTP_200_OK)
async  def get_task(id:int):
    task_by_id = None
    for task in task_list:
        if task.id == id:
            task_by_id = task
    if task_by_id is None:
        raise HTTPException(status_code= 404, detail="Task not found")
    return  task_by_id


@router.put("/tasks/{id}", status_code = status.HTTP_200_OK)
async def update_task(id:int, task:Task):
    if task.id != id | id not in task_list:
        raise HTTPException(status_code=404, detail="Task not found")
    task_list[id -1] = task
    return task_list

@router.delete("/tasks/{id}", status_code=status.HTTP_200_OK)
async def delete_task(id:int):
    for t in task_list:
        if t.id == id:
            task_list.remove(t)
            return {}

    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/reset/", status_code=status.HTTP_200_OK)
async def reset_tasks():
    task_list.clear()