from fastapi.testclient import TestClient
from be_python_assessment.configs.configs import ServiceSettings
from be_python_assessment.models.breeds import Breed
from be_python_assessment.services.breeds import app, setup_app

setup_app(ServiceSettings("breeds"))
client = TestClient(app)

# In addtion to writing some tests, I also did a whole lot of 
# clicking around in Postman.

def test_get_breeds():
  response = client.get("/api/breeds/", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 200
  assert len(response.json()) >= 1

def test_get_breeds_with_filter():
  response = client.get("/api/breeds?pt=0", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 200

  for breed in response.json():
    assert breed["petType"] == 0

def test_get_dog_breeds():
  response = client.get("/api/breeds/dogs/15", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 200
  assert Breed.model_validate(response.json())

def test_get_cat_breeds():
  response = client.get("/api/breeds/cats/475", headers={"X-Token": "coneofsilence"})
  assert response.status_code == 200
  assert Breed.model_validate(response.json())