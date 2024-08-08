from abc import ABC
from common.base_response import BaseResponse

class FetchResponse(BaseResponse, ABC):
  def __init__(self, logger, ssh, config:dict):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.ssh = ssh
    unknown_mods = self.check_schema(config, schema={
      'ls': {}
    })
    if unknown_mods != set():
      self.log.error('Unknown mods {} found in data.'.format(unknown_mods))
    self.config = config
    self.check_which(self.config)

  def fetch(self):
    self.log.fn = self.__class__.__name__ + '.' + self.fetch.__name__
    state = {}
    for mod, names in self.config.items():
      state[mod] = {}
      if mod == 'ls':
        for name, param in names.items():
          status, output = self.ssh.run('ls -lAG ' + param['path'], None)
          if status == 0:
            state[mod][name] = param
            state[mod][name]['output'] = output
          else:
            self.log.error('mod {} returned status code {}.'.format(mod, status))
    self.state = state
