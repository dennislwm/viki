from abc import ABC
from common.base_response import BaseResponse

class ApplyResponse(BaseResponse, ABC):
  def __init__(self, logger, ssh, insert:dict, remove:dict, state:dict):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.ssh = ssh
    self.delta_insert = insert
    self.delta_remove = remove
    self.state = state

  def apply_insert(self):
    self.log.fn = self.__class__.__name__ + '.' + self.apply_insert.__name__
    state = {}
    for mod, names in self.delta_insert.items():
      state[mod] = {}
      if mod == 'wget':
        for name, param in names.items():
          status, output = self.ssh.run('wget -O ' + param['output'] + ' ' + param['url'], None)
          if status == 0:
            self.state[mod][name] = param
            self.log.info('{} : {}'.format(name, self.state[mod][name]))
          else:
            self.log.error('mod {} returned status code {}.'.format(mod, status))

  def apply_remove(self):
    self.log.fn = self.__class__.__name__ + '.' + self.apply_remove.__name__
    for mod, names in self.delta_remove.items():
      if mod == 'wget':
        for name in names.keys():
          if name in self.state[mod]:
            status, output = self.ssh.run('rm ' + self.state[mod][name]['path'] + '/' + self.state[mod][name]['output'], None)
            if status == 0:
              self.log.info('{} : {}'.format(name, self.state[mod][name]))
              del self.state[mod][name]
            else:
              self.log.error('mod {} returned status code {}.'.format(mod, status))
