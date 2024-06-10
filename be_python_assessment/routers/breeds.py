import re

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, status

from ..models.common import PetTypeEnum
from ..db.mockdb import MockDB
from ..models.breeds import Breed

router = APIRouter(
  prefix="/api/breeds",
  tags=["breeds"],
)

@router.get("/")
async def getBreeds(request: Request, pt: Optional[PetTypeEnum] = None) -> list[Breed]:
  db = request.state.db

  # I considered moving this query param functionality to 
  # /breeds/dogs and breeds/cats.
  if pt is not None:
    return db.readBreedsByType(pt)
  else:
    return db.readAllBreeds()

# Decided to lookup by breed id instead of breed name.
@router.get("/dogs/{id}")
async def getDogBreeds(id: int, request: Request) -> Breed:
  db = request.state.db

  return getBreed(db, PetTypeEnum.dog, id)


@router.get("/cats/{id}")
async def getCatBreeds(id: int, request: Request) -> Breed:
  db = request.state.db

  return getBreed(db, PetTypeEnum.cat, id)


def getBreed(db: MockDB, petType: PetTypeEnum, id:int) -> Breed:
  # I found a bug in the regular expression that was here and fixed it (it tried
  # to reference a group that didn't exist). Then I made an expression to account
  # for breed names with spaces. It worked but it seems less future-proof/scalable
  # to me compared to looking up by breed ID, a primary key. 
  try:
    breed = db.readBreed(petType, id)
  except:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="breed name does not exist"
    )

  return breed
