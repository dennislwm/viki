from abc import ABC, abstractmethod
import json

class BaseResponse(ABC):
  def __init__(self, logger):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.ssh = None
    self.config: dict = {}

  def check_schema(self, config:dict, schema:dict) -> dict:
    self.log.fn = self.__class__.__name__ + '.' + self.check_schema.__name__
    config_keys = set(config.keys())
    schema_keys = set(schema.keys())
    return config_keys - schema_keys

  def pretty_json(self, config:dict) -> str:
    self.log.fn = self.__class__.__name__ + '.' + self.pretty_json.__name__
    return json.dumps(config, indent=4)

  def check_which(self, config:dict):
    self.log.fn = self.__class__.__name__ + '.' + self.check_which.__name__
    for mod, names in self.config.items():
      status, output = self.ssh.run('which ' + mod, None)
      if status == 0:
        self.log.info('mod {} returned status code {} and {}'.format(mod, status, output))
      else:
        self.log.error('mod {} returned status code {}.'.format(mod, status))
