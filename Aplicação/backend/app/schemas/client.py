from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    project_id: int
    communication_level: str = "standard"

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    project_id: Optional[int] = None
    communication_level: Optional[str] = None

class ClientInDB(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ClientWithProject(Client):
    project: dict = {}

class ClientSummary(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    project_name: str

class ClientBulkCreate(BaseModel):
    clients: List[ClientCreate]

class ClientBulkUpdate(BaseModel):
    clients: List[ClientUpdate]

class ClientResponse(Client):
    pass