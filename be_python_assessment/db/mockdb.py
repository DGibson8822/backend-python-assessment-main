import json
import os
import uuid

from typing import Dict, List

from ..configs.configs import ServiceSettings
from ..models.breeds import Breed
from ..models.common import PetTypeEnum
from ..models.pets import PetCreate, PetWithId, PetPartial

from fastapi import Response

class MockDB():
  collectionName: str
  breedsData: Dict[PetTypeEnum, Dict[int, Breed]] = {}
  #TODO: Add pets data to the Mock DB
  # Dominique Gibson:
  # Having IDs at the top level means I can "query" by ID,
  # which will be handy for the pets PATCH route since a PATCH
  # request body won't necessarily have the PetType field.
  petsData: Dict[str, PetWithId] = {}

  def __init__(self, config: ServiceSettings):
    project_root = os.path.dirname(os.path.dirname(__file__))
    file = open(project_root + config.dataFile)
    jsonData = json.load(file)

    match config.collectionName:
      case "breeds":
        data: Dict[PetTypeEnum, Dict[int, Breed]] = {
          PetTypeEnum.dog: {},
          PetTypeEnum.cat: {},
        }

        for breedData in jsonData:
          match breedData["petType"]:
            case PetTypeEnum.dog:
              data[PetTypeEnum.dog][breedData["id"]] = breedData
            case PetTypeEnum.cat:
              data[PetTypeEnum.cat][breedData["id"]] = breedData

        self.breedsData = data
      
      case "pets":
        data: Dict[str, PetWithId] = {}

        for petData in jsonData:
          data[petData["id"]] = petData
        self.petsData = data

  def connect(self) -> bool:
    return True

  def disconnect(self) -> bool:
    return True

  def readAllBreeds(self) -> List[Breed]:
    breeds: List[Breed] = []

    dogBreeds = self.breedsData[PetTypeEnum.dog]
    catBreeds = self.breedsData[PetTypeEnum.cat]

    for _, data in dogBreeds.items():
      breeds.append(data)

    for _, data in catBreeds.items():
      breeds.append(data)

    return breeds

  def readBreedsByType(self, petType: PetTypeEnum) -> List[Breed]:
    match petType:
      case PetTypeEnum.dog:
        filteredData = self.breedsData[petType]
      case PetTypeEnum.cat:
        filteredData = self.breedsData[petType]
      case _:
        raise Exception("no breeds data found")

    breeds:List[Breed] = []

    for _, data in filteredData.items():
      breeds.append(data)
    return breeds

  def readBreed(self, petType: PetTypeEnum, id: int) -> Breed:
    petTypeData = self.breedsData[petType]

    if len(petTypeData) > 0:
      if id in petTypeData:
        return petTypeData[id]
      else:
        raise Exception("breed data does not exist")

    raise Exception("no breeds data found")

  #TODO: Add mock db function to be able to create/update pet data into the database
  def createPet(self, petData: PetCreate) -> PetWithId:
    # Generate a primary key, add it to the pet model.
    new_id = str(uuid.uuid4())
    pet = PetWithId(id=new_id, **petData.model_dump()).model_dump()
    # Perform database insert
    self.petsData[new_id] = pet
    return pet
  
  # Had to import the Response object for this, as FastAPI returns JSON by default,
  # which does not conform to typical 204 status behavior.
  def patchPet(self, petData: PetPartial) -> Response:
    id = petData.model_dump()['id']
    self.petsData[id].update(petData.model_dump(exclude_unset=True))
    return Response(
            content=None,
            status_code=204,
            headers=None,
            media_type=None,
            background=None,
          )
  