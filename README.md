# Regarding My Proposed Changes

In addition to implementing the required API functionality specified for this project, I've taken the liberty of making best practices and code quality improvements as well. I go into detail in the code comments in the relevant sections, but examples that come to mind include:

- Using breed ID in the url parameter rather than breed name for the route `@router.get("/dogs/{id}")`. Using breed name effectively would require a standard for what characters are allowed and regular expression for url encoding of spaces and special characters, which seems less scalable and future-proof given the limited information. Breed ID is a primary key in the database so uniqueness is guaranteed and it only inlcudes alphanumeric characters.
- Instatiating the MockDB object outside of the middleware function where it originally resided, rather than within. Before this change, the database was re-initialized upon each request. Now it is only intialized when the service first starts, and any changes to the data persists.
- The breeds and pets APIs each had their own service launcher file. The logic in both was very similar, so I combined the them into a single file that uses the --servce argument passed from the terminal to determine which API service to start. This makes the code more DRY, though I can also see an argument for keeping things separate in the interest of "separation of concerns", depending on how these services would be hosted in prod.

# Assessment

Welcome to Wagmo and the backend software engineer tech assessment. The purpose of this exercise is
to give you the opportunity to show us how you would solve a feature that you may be asked to implement.
in the role. In order to start the assessment unzip the code and download the dependencies. We will be
looking for good coding practices and a design that will be able to scale.

# Getting Started

If you do not currently have python installed or updated to version 3.12 follow the installation
instructions at [python install](https://www.python.org/downloads/release/python-3123/) or if you have homebrew setup you can run `brew install python@3.12`. Then [setup poetry](https://python-poetry.org/docs/)

Once python & poetry are setup, you can run:

- `poetry install` to install dependencies
- `poetry run start --service [breeds or pets]` to start the webserver
- `poetry run pytest` to run tests

You may update the `configs/conf.yml` file to change service ports, the data
file to read for the breeds service.

## Part 1 (Breeds Service)

Go through this code base and understand the breeds service. This service is used to retrieve breed
information and can be used to validate a breed that is selected by a customer for their pet. Make
sure to test edge cases, either by using a tool like Postman or creating additional unit tests.
Debug this endpoint is working as expected and fix/redesign any section of the code you see fit.

The purpose of this part of the assessment is to test your ability to find and fix bugs in code that
has already been written. When testing the breeds service there is one critical bug that will cause using
this service for validation to fail. The validation use case to call the breeds service to return a single breed.
If a breed does not exist a 404 is returned.

The endpoint will handle the following calls:

```
1. http://localhost:8000/api/breeds
2. http://localhost:8000/api/breeds?pt=0
3. http://localhost:8000/api/breeds/dogs/:breedname
4. http://localhost:8000/api/breeds/cats/:breedname
```

The expected return values on succss will be:

```
#/api/breeds or /api/breeds?pt=0
[
    {
        "name": "Bernese Mountain Dog",
        "petType": 0,
        "id": 64
    },
    {
        "name": "Central Asian Shepherd Dog",
        "petType": 0,
        "id": 110
    },
    {
        "name": "Tosa",
        "petType": 0,
        "id": 428
    },
    {
        "name": "Alsatian",
        "petType": 0,
        "id": 15
    },
    {
        "name": "Bulldog",
        "petType": 0,
        "id": 97
    },
    {
        "name": "Dutch Shepherd",
        "petType": 0,
        "id": 164
    },
    ...
]

# /api/breeds/dogs/:breedName
{
    "name": "Bulldog",
    "petType": 0,
    "id": 97
}

# /api/breeds/cats/:breedName
{
    "name": "Colorpoint",
    "petType": 1,
    "id": 481
}
```

MockDB currently reads the json files in `./data/`. You can add or remove data by editing the provided json files, or you can create your own. If creating your own make sure to follow the same format.

## Part 2

The second part we are asking you to create your own service to allow a customer to add/update
their pet. This part of the assessment we are looking for you to add to this code base. We will be
looking for this endpoint to adhere to the followingacceptance criteria.

- An endpoint `/api/pets` is used by pets service router
- The endpoint is expected to take in a request provided in the below example
- The endpoint should return the appropriate status code and pet data when one is created
- The call should handle errors appropriately

### Note

There is already boilerplate code here for you to get started. Make sure to add logic to the TODOs.

### Example Request

```
POST /api/pets
{
    "name": "Cooper",
    "breed": "Golden Retriever",
    "petType": "dog",
    "dob": "2020-06-20",
    "sterilized": true,
    "user": "john.doe@example.com"
}

PATCH /api/pets
{
    "id": 1
    "dob": "2021-06-20",
}
```

### Example Response

```
POST /api/pets 201
{
    "id": 1,
    "name": "Cooper",
    "breed": "Golden Retriever",
    "petType": "dog",
    "dob": "2020-06-20",
    "sterilized": true,
    "user": "john.doe@example.com"
}

PATCH /api/pets 204
```
