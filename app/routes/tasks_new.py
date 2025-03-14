from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.utils import SECRET_KEY, ALGORITHM
from app.models import PriorityEnum, StatusEnum

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Auth section
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# Pydantic Models
class TaskBase(BaseModel):
    title: str
    description: str
    email: str
    due_date: date
    priority: PriorityEnum
    status: StatusEnum

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

# In-memory storage for demo purposes
tasks_db = []
task_id_counter = 1

# Endpoints

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    global task_id_counter
    new_task = task.model_dump()
    new_task["id"] = task_id_counter
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task

@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(
    current_user: str = Depends(get_current_user),
    priority: Optional[PriorityEnum] = Query(None, description="Filter tasks by priority"),
    status: Optional[StatusEnum] = Query(None, description="Filter tasks by status"),
    search: Optional[str] = Query(None, description="Search in title or description")
):
    filtered_tasks = tasks_db.copy()
    
    if priority:
        filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]
    
    if status:
        filtered_tasks = [task for task in filtered_tasks if task["status"] == status]
    
    if search:
        search = search.lower()
        filtered_tasks = [
            task for task in filtered_tasks 
            if search in task["title"].lower() or 
               search in task["description"].lower()
        ]
    
    return filtered_tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_single_task(task_id: int, current_user: str = Depends(get_current_user)):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, current_user: str = Depends(get_current_user)):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db[index].update(updated_task.model_dump())
            return tasks_db[index]
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: str = Depends(get_current_user)):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            deleted_task = tasks_db.pop(index)
            return {"message": "Task deleted successfully", "task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")
