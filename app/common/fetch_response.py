from abc import ABC
from common.base_response import BaseResponse
from common.ssh_command import DATA_COMMAND, ssh_command

class FetchResponse(BaseResponse, ABC):
  def __init__(self, logger, ssh, config:dict, vars:dict):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.ssh = ssh
    self.sudo_password = None
    if 'sudo_password' in vars and vars['sudo_password'] != '':
      self.sudo_password = vars['sudo_password']
    unknown_mods = self.check_schema(config, schema=DATA_COMMAND)
    if unknown_mods != set():
      self.log.error('Unknown mods {} found in data.'.format(unknown_mods))
    self.config = config
    self.check_which(self.config)

  def fetch(self):
    self.log.fn = self.__class__.__name__ + '.' + self.fetch.__name__
    state = {}
    for mod, names in self.config.items():
      state[mod] = {}
      cmd = DATA_COMMAND[mod]
      for name, param in names.items():
        self.log.info('{}'.format(ssh_command(cmd, param)))
        exec = ssh_command(cmd, param, self.sudo_password)
        if exec[:4] == "sudo":
          status, output = self.ssh.run(exec, self.sudo_password)
        else:
          status, output = self.ssh.run(exec, None)
        if status == 0:
          state[mod][name] = param
          state[mod][name]['output'] = output
        else:
          self.log.error('mod {} returned status code {}.'.format(mod, status))
    self.state = state
