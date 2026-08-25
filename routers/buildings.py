from fastapi import APIRouter, Depends

from dependencies import verify_api_key
from database import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.buildings import Building

from schemas.buildings import BuildingInfo

router = APIRouter()


@router.get("/buildings", response_model=list[BuildingInfo], dependencies=[Depends(verify_api_key)])
async def get_buildings(session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Building))
    result = statement.scalars().all()

    return result