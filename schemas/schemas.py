
from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class TransactionSchema(BaseModel):
    user: int

    class Config:
        from_attributes=True

    
class LoginSchema(BaseModel):
    email: str
    password:str
    
    class Config:
        from_attributes=True

class ResponseTransactionSchema(BaseModel):
    id: int
    status: str
    amount: float
    
    class Config:
        from_attributes=True