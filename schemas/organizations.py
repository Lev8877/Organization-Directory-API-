from pydantic import BaseModel, ConfigDict

class OrganizationInfo(BaseModel):
    id: int
    name: str 

    model_config = ConfigDict(from_attributes=True)

class ResponseOrganizationInfo(BaseModel):
    id: int 
    name: str 
    address: str 
    phones: list[str]
    activities: list[str]

    model_config = ConfigDict(from_attributes=True)