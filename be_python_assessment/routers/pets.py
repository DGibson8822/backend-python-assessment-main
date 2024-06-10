import re

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, status, Response

from ..models.common import PetTypeEnum
from ..db.mockdb import MockDB
from ..models.pets import PetCreate, PetWithId, PetPartial

router = APIRouter(
  prefix="/api/pets",
  tags=["pets"],
)

@router.post("/", status_code=201)
async def createPet(request: Request, petData: PetCreate) -> PetWithId:
  db = request.state.db

  return db.createPet(petData)

@router.patch("/", status_code=204)
async def updatePetPartial(request: Request, petData: PetPartial) -> Response:
  db = request.state.db

  return db.patchPet(petData)


