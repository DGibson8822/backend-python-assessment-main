from fastapi import FastAPI, Request, Response

from ..db.mockdb import MockDB
from ..routers import breeds, health
from ..configs import configs

import uvicorn

app = FastAPI()

def setup_app(settings: configs.ServiceSettings):
  app.include_router(health.router)
  app.include_router(breeds.router)
  # is there a better way to setup mock database?
  # currently we create a new instance of mockdb on every request
  # Dominique Gibson:
  # With db setup here, we no longer create a new instance on every request.
  # This also allows newly POSTed data to persist while the server is up.
  db = MockDB(settings)
  @app.middleware("http")
  async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
      request.state.db = db
    except Exception as e:
      print("error setting up mockdb with exception: ", e)

    try:
      response = await call_next(request)
    finally:
      request.state.db.disconnect()
    return response

def start(settings: configs.ServiceSettings):
  setup_app(settings)
  config = uvicorn.Config("be_python_assessment.services.breeds:app", host="0.0.0.0", port=settings.port, reload=True)
  server = uvicorn.Server(config)
  server.run()
