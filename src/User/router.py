from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete

from User.models import User
from User.schemas import UserRead, UserCreate, UserUpdate, UserDelete
from database import get_async_session

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/{user_id}", response_model=Union[UserRead, None])
async def read_user(user_id: int, session=Depends(get_async_session)) -> Union[UserRead, None]:
    query = select(User).where(User.id == user_id)
    user = await session.execute(query)
    user = user.fetchone()
    if not user:
        return
    user_read = UserRead.from_orm(user[0])
    return user_read


@router.post("/", response_model=Union[UserRead, None])
async def create_user(user: UserCreate, session=Depends(get_async_session)) -> Union[UserRead, None]:
    new_user = User(**user.dict())
    session.add(new_user)
    await session.commit()
    return UserRead.from_orm(new_user)


@router.put("/", response_model=Union[UserRead, None])
async def update_user(user: UserUpdate, session=Depends(get_async_session)) -> Union[UserRead, None]:
    query = select(User).where(User.id == user.id)
    current_user = await session.execute(query)
    current_user = current_user.scalar()
    if current_user:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            if value:
                setattr(current_user, key, value)
        await session.commit()
        return UserRead.from_orm(current_user)
    else:
        return None


@router.delete("/")
async def update_user(user: UserDelete, session=Depends(get_async_session)) -> dict:
    query = delete(User).where(User.id == user.id)
    await session.execute(query)
    await session.commit()
    return {"detail": f"User {user.id} deleted"}
