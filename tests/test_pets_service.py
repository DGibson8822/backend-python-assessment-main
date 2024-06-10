from fastapi.testclient import TestClient
from be_python_assessment.configs.configs import ServiceSettings
from be_python_assessment.models.pets import PetWithId
from be_python_assessment.services.pets import app, setup_app

setup_app(ServiceSettings("pets"))
client = TestClient(app)

# In addtion to writing some tests, I also did a whole lot of 
# clicking around in Postman.

def test_create_pet_success():
  response = client.post(
                "/api/pets/", 
                headers={"X-Token": "coneofsilence"},
                json={
                  "name": "Cooper",
                  "breed": "Golden Retriever",
                  "petType": 0,
                  "dob": "2020-06-20",
                  "sterilized": True,
                  "user": "john.doe@example.com"
              })
  assert response.status_code == 201
  assert PetWithId.model_validate(response.json())

def test_create_pet_fail():
  response = client.post(
                "/api/pets/", 
                headers={"X-Token": "coneofsilence"},
                json={
                  "breed": "Golden Retriever",
                  "petType": 0,
                  "dob": "2020-06-20",
                  "sterilized": True,
                  "user": "john.doe@example.com"
              })
  assert response.status_code == 422

def test_patch_pet_success():
  response = client.patch(
                "/api/pets/", 
                headers={"X-Token": "coneofsilence"},
                json={
                  "id": "uuid-1",
                  "user": "updated_email"
              })
  assert response.status_code == 204

def test_patch_pet_fail():
  response = client.patch(
                "/api/pets/", 
                headers={"X-Token": "coneofsilence"},
                json={
                  "user": "updated_email"
              })
  assert response.status_code == 422
