import re
from pydantic import BaseModel
from datetime import datetime

class Usuarios(BaseModel):
    username: str
    password: str

class UsuariosRequest(Usuarios):
    username: str
    password: str

class TokenData(BaseModel):
    access_token: str
    expires_at: datetime

class UsuariosResponse(Usuarios):
    username: str
    password: str
    class Config:
        from_attributes=True    
        orm_mode = True
