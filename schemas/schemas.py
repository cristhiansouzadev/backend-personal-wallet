
from pydantic import BaseModel
from typing import Optional, List

    
class LoginSchema(BaseModel):
    email: str
    password:str
    
    class Config:
        from_attributes=True

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
    type_flow: str
    category: str
    amount: float

    class Config:
        from_attributes=True

class ResponseTransactionSchema(BaseModel):
    id: int
    status: str
    amount: float
    
    class Config:
        from_attributes=True


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes=True

class ResponseCategorySchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes=True