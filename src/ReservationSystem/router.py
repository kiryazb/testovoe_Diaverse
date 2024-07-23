from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ReservationSystem.models import ReservationBook
from ReservationSystem.schemas import ReservationCreate, ReservationUpdate
from ReservationSystem.utils import long_operation
from database import get_async_session

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"]
)


@router.post("/")
async def create_reservation(request: ReservationCreate,
                             session: AsyncSession = Depends(get_async_session)) -> dict:
    if request.date_from < datetime.now().date() or request.date_to < request.date_from:
        raise HTTPException(status_code=400, detail="Invalid dates")

    query = select(ReservationBook.id).where(
        and_(ReservationBook.book_id == request.book_id, ReservationBook.date_from <= request.date_from,
             ReservationBook.date_to >= request.date_to))

    result = await session.execute(query)
    result = result.fetchall()

    if result:
        raise HTTPException(status_code=409, detail="Reservation already exists for this date")

    reservation = ReservationBook(**request.dict())
    session.add(reservation)
    await session.commit()

    return {"status": 200,
            "detail": reservation}


@router.put("/")
async def change_deadline_date(request: ReservationUpdate, session: AsyncSession = Depends(get_async_session)) -> dict:
    order = await session.execute(select(ReservationBook).where(ReservationBook.id == request.id))
    order = order.scalar()
    if request.date_to >= order.date_to or request.date_to <= order.date_from:
        raise HTTPException(status_code=400, detail="Invalid dates")
    order.date_to = request.date_to
    await session.commit()
    return {"status": 200,
            "details": order}


@router.get("/celery")
def celery_task() -> dict:
    long_operation.delay()
    return {"status": 200}
