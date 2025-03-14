from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(str, Enum):
    NOT_STARTED = "Not started"
    PENDING = "Pending"
    COMPLETED = "Completed"

class Task(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    due_date: datetime
    priority: PriorityEnum
    status: StatusEnum = StatusEnum.NOT_STARTED

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(v):
            raise ValueError("Invalid email format. Please provide a valid email address.")
        
        # Additional validations similar to Joi
        parts = v.split("@")
        if len(parts) != 2:
            raise ValueError("Email must contain exactly one @ symbol")
        
        local_part, domain = parts
        if not local_part or not domain:
            raise ValueError("Email local part and domain must not be empty")
            
        if len(local_part) > 64:
            raise ValueError("Email local part must not exceed 64 characters")
            
        if len(domain) > 255:
            raise ValueError("Email domain must not exceed 255 characters")
            
        if not all(part and len(part) <= 63 for part in domain.split(".")):
            raise ValueError("Each DNS label in email domain must not exceed 63 characters")
        
        return v
