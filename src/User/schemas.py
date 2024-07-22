from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int
    name: str
    second_name: str
    avatar: bytes


class UserRead(BaseModel):
    id: int
    name: str
    second_name: str
    avatar: bytes | None

    class Config:
        orm_mode = True
        from_attributes = True


class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    second_name: Optional[str] = None
    avatar: Optional[bytes] = None


class UserDelete(BaseModel):
    id: int
