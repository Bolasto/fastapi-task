from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date
from app.utils import SECRET_KEY, ALGORITHM
from app.models import PriorityEnum, StatusEnum
from app.database import tasks_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

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
from datetime import datetime
from pydantic import field_validator

class TaskBase(BaseModel):
    title: str
    description: str
    email: EmailStr
    due_date: str
    priority: PriorityEnum = PriorityEnum.LOW  # Set default value
    status: StatusEnum = StatusEnum.NOT_STARTED  # Set default value

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title cannot be longer than 100 characters')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

    @field_validator('due_date')
    @classmethod
    def validate_date(cls, v):
        try:
            if not v.strip():
                raise ValueError('Due date cannot be empty')
            # Parse the date string to ensure it's valid
            datetime.strptime(v.strip(), '%Y-%m-%d')
            return v.strip()
        except ValueError as e:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: str

# MongoDB is used for storage, no need for in-memory variables

# Endpoints

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    try:
        # Log incoming task data
        logger.info(f"Creating task with data: {task.model_dump_json()}")
        
        # Check for duplicate title
        existing_task = await tasks_collection.find_one({"title": task.title})
        if existing_task:
            logger.warning(f"Duplicate task title found: {task.title}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A task with this title already exists"
            )

        # Convert task to dict and add user
        task_dict = task.model_dump()
        task_dict["user"] = current_user
        logger.info(f"Prepared task dict: {task_dict}")
        
        try:
            # Attempt to insert into MongoDB
            result = await tasks_collection.insert_one(task_dict)
            if not result.inserted_id:
                logger.error("MongoDB insert succeeded but no ID returned")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create task in database"
                )
                
            # Add ID to response
            task_dict["id"] = str(result.inserted_id)
            logger.info(f"Successfully created task with ID: {task_dict['id']}")
            return task_dict
            
        except Exception as db_error:
            logger.error(f"MongoDB error: {str(db_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(db_error)}"
            )
            
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error creating task: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the task"
        )

@router.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(
    current_user: str = Depends(get_current_user),
    priority: Optional[PriorityEnum] = Query(None, description="Filter tasks by priority"),
    status: Optional[StatusEnum] = Query(None, description="Filter tasks by status"),
    search: Optional[str] = Query(None, description="Search in title or description")
):
    # Build the query filter
    query = {"user": current_user}  # Only show tasks for the current user
    
    if priority:
        query["priority"] = priority
    
    if status:
        query["status"] = status
    
    if search:
        search = search.lower()
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = tasks_collection.find(query)
    tasks = []
    async for document in cursor:
        document["id"] = str(document["_id"])
        del document["_id"]
        tasks.append(document)
    
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_single_task(task_id: str, current_user: str = Depends(get_current_user)):
    try:
        task = await tasks_collection.find_one({"_id": ObjectId(task_id), "user": current_user})
        if task:
            task["id"] = str(task["_id"])
            del task["_id"]
            return task
    except:
        pass
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, updated_task: TaskCreate, current_user: str = Depends(get_current_user)):
    # Check if the new title already exists in another task
    existing_task = await tasks_collection.find_one(
        {"title": updated_task.title, "_id": {"$ne": ObjectId(task_id)}}
    )
    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A task with this title already exists"
        )

    task_dict = updated_task.model_dump()
    result = await tasks_collection.update_one(
        {"_id": ObjectId(task_id), "user": current_user},
        {"$set": task_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: str = Depends(get_current_user)):
    result = await tasks_collection.find_one_and_delete(
        {"_id": ObjectId(task_id), "user": current_user}
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
        
    result["id"] = str(result["_id"])
    del result["_id"]
    return {"message": "Task deleted successfully", "task": result}
