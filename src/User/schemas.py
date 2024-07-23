from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    second_name: str
    avatar: bytes


class UserCreate(BaseModel):
    pass


class UserRead(BaseModel):
    pass

    class Config:
        orm_mode = True
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    second_name: Optional[str] = None
    avatar: Optional[bytes] = None


class UserDelete(User):
    pass
