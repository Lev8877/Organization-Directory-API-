from fastapi import FastAPI 

import models

from routers.buildings import router as organizations_router
from routers.organizations import router as buildings_router

app = FastAPI()

app.include_router(organizations_router)
app.include_router(buildings_router)

