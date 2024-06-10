from .services import breeds, pets, service_launcher
from .configs import configs
import click

@click.command()
@click.option(
  "--service",
  help="enter a service to start (breeds or pets)",
  type=str
)
# def init(service):
#   match service:
#     case "breeds":
#       breeds.start(configs.ServiceSettings("breeds"))
#     case "pets":
#       pets.start(configs.ServiceSettings("pets"))
#     case _:
#       print("invalid service selected")

def init(service):
  match service:
    case "breeds":
      service_launcher.start(configs.ServiceSettings("breeds"))
    case "pets":
      service_launcher.start(configs.ServiceSettings("pets"))
    case _:
      print("invalid service selected")
