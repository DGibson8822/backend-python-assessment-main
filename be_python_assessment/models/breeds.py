from pydantic import BaseModel, ValidationError
from .common import PetTypeEnum

class Breed(BaseModel):
  id: int
  name: str
  petType: PetTypeEnum