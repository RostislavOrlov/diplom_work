import datetime
from enum import Enum

from pydantic import BaseModel


class TaskPriority(Enum):
    important = 'important'
    not_important = 'not_important'


class TaskStatus(Enum):
    complete = 'complete'
    in_process = 'in_process'
    deferred = 'deferred'


class TeamProject(BaseModel):
    team_id: int
    name: str
    description: str


class TeamTask(BaseModel):
    name: str
    description: str
    status: TaskStatus
    priority: TaskPriority


class TeamMember(BaseModel):
    id: int
    team_id: int
    user_id: int
    role_id: int


class TeamDTO(BaseModel):
    id: int
    name: str
    description: str
    img_profile_ref: str
    team_ref: str
    user_creator_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
