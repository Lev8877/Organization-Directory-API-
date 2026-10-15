
    
  
from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import verify_api_key
from database import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, func
from sqlalchemy.orm import selectinload
from geoalchemy2 import Geography

from models.organizations import Organization
from models.activity import Activity
from models.buildings import Building

from services.organizations import get_activity_tree

from schemas.organizations import OrganizationInfo, ResponseOrganizationInfo

router = APIRouter()


@router.get("/organizations/building/{building_id}", response_model=list[OrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organizations_by_building_id(building_id: int, session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Organization).where(Organization.building_id == building_id))
    result = statement.scalars().all()

    return result

@router.get("/organizations/activity/simple/{activity_id}", response_model=list[OrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organizations_by_activity_id(activity_id: int, session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Organization).join(Organization.activities).where(Activity.id == activity_id))
    result = statement.scalars().all()

    return result

@router.get("/organization/info/id/{organization_id}", response_model=ResponseOrganizationInfo, dependencies=[Depends(verify_api_key)])
async def get_organization_info_by_organization_id(organization_id: int, session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Organization).where(Organization.id == organization_id).options(selectinload(Organization.building), selectinload(Organization.phones), selectinload(Organization.activities)))
    organization = statement.scalar_one_or_none()

    if organization is None:
        raise HTTPException(status_code=404, detail="Организации с таким id не существует")

    result = {
        "id": organization.id,
        "name": organization.name,
        "address": organization.building.address,
        "phones": [phone.phone for phone in organization.phones],
        "activities": [activity.name for activity in organization.activities]
    }

    return result

@router.get("/organization/info/name/{organization_name}", response_model=list[ResponseOrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organization_info_by_organization_name(organization_name: str, session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Organization).where(Organization.name == organization_name.strip()).options(selectinload(Organization.building), selectinload(Organization.phones), selectinload(Organization.activities)))
    organizations = statement.scalars().all()

    if not organizations:
        raise HTTPException(status_code=404, detail="Организации с таким названием не существует")

    result = []

    for organization in organizations:
        result.append({
            "id": organization.id,
            "name": organization.name,
            "address": organization.building.address,
            "phones": [phone.phone for phone in organization.phones],
            "activities": [activity.name for activity in organization.activities]
        })

    return result

@router.get("/organizations/in_square", response_model=list[OrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organizations_in_square(min_latitude: float = Query(ge=-90, le=90), max_latitude: float = Query(ge=-90, le=90), min_longitude: float = Query(ge=-180, le=180), max_longitude: float = Query(ge=-180, le=180), session: AsyncSession = Depends(get_session)):
    if min_longitude > max_longitude or min_latitude > max_latitude:
        raise HTTPException(status_code=422, detail="Минимальные значения не могут быть больше максимальных")

    statement = await session.execute(select(Organization).join(Organization.building).where(Building.latitude.between(min_latitude, max_latitude), Building.longitude.between(min_longitude, max_longitude)))
    organizations = statement.scalars().all()

    return organizations

@router.get("/organizations/in_radius", response_model=list[OrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organizations_in_radius(latitude: float = Query(ge=-90, le=90), longitude: float = Query(ge=-180, le=180), radius: float = Query(gt=0), session: AsyncSession = Depends(get_session)):
    building_point = cast(func.ST_SetSRID(func.ST_MakePoint(Building.longitude, Building.latitude), 4326), Geography(srid=4326))
    center_point = cast(func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326), Geography(srid=4326))

    statement = await session.execute(select(Organization).join(Organization.building).where(func.ST_DWithin(building_point, center_point, radius)))

    return statement.scalars().all()

@router.get("/organizations/activity/{activity_id}", response_model=list[OrganizationInfo], dependencies=[Depends(verify_api_key)])
async def get_organizations_by_activity(activity_id: int, session: AsyncSession = Depends(get_session)):
    statement = await session.execute(select(Activity).where(Activity.id == activity_id).options(selectinload(Activity.children).selectinload(Activity.children)))
    activity = statement.scalar_one_or_none()

    if activity is None:
        raise HTTPException(status_code=404, detail="Переданного вами id активности не существует")

    activities = get_activity_tree(activity)
    activity_ids = [activity.id for activity in activities]

    statement = await session.execute(select(Organization).join(Organization.activities).where(Activity.id.in_(activity_ids)))
    organizations = statement.scalars().unique().all()

    return organizations

