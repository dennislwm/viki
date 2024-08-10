from abc import ABC
from common.base_response import BaseResponse
from common.ssh_command import MODS_COMMAND

class PlanResponse(BaseResponse, ABC):
  def __init__(self, logger, ssh, config:dict, state:dict):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.ssh = ssh
    unknown_mods = self.check_schema(config, schema=MODS_COMMAND)
    if unknown_mods != set():
      self.log.error('Unknown modules {} found in mods.'.format(unknown_mods))
    self.config = config
    self.check_which(self.config)
    self.state = state
    self.delta_insert = self.__delta_insert()
    self.count_insert = self.__delta_count(self.delta_insert)
    self.delta_remove = self.__delta_remove()
    self.count_remove = self.__delta_count(self.delta_remove)

  def __delta_insert(self) -> dict:
    self.log.fn = self.__class__.__name__ + '.' + self.__delta_insert.__name__
    delta = {}
    for mod, names in self.config.items():
      state = self.state if mod in self.state else { mod: {} }
      add = self.check_schema(names, state[mod])
      delta[mod] = dict.fromkeys(add, 0)
      for name, param in names.items():
        if name in delta[mod]:
          delta[mod][name] = param
    return delta

  def __delta_remove(self) -> dict:
    self.log.fn = self.__class__.__name__ + '.' + self.__delta_remove.__name__
    delta = {}
    for mod, names in self.config.items():
      state = self.state if mod in self.state else { mod: {} }
      remove = self.check_schema(state[mod], names)
      delta[mod] = dict.fromkeys(remove, 0)
      for name, param in names.items():
        if name in delta[mod]:
          delta[mod][name] = param
    return delta

  def __delta_count(self, delta:dict) -> int:
    sum = 0
    for mod, names in delta.items():
      sum = sum + len(names.items())
    return sum