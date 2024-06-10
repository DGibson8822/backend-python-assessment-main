from typing import Optional
from pydantic_settings import BaseSettings
import yaml
import os

class ServiceSettings(BaseSettings):
  dbName: str = ""
  collectionName: str = ""
  env: str = ""
  useMongo: str = ""
  port: int = -1
  dataFile: str = ""

  def __init__(self, service_name: str):
    super().__init__()
    yaml_settings = dict()
    submodule_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(submodule_path, "conf.yml")) as f:
      yaml_settings.update(yaml.load(f, Loader=yaml.FullLoader))

    self.dbName = yaml_settings['services'][service_name]['dbName']
    self.collectionName = yaml_settings['services'][service_name]['collectionName']
    self.port = int(yaml_settings['services'][service_name]['port'])
    self.dataFile = yaml_settings['services'][service_name]['dataFile']

