from abc import ABC
from common.base_response import BaseResponse
from common.ssh_command import MODS_COMMAND, ssh_command

class ApplyResponse(BaseResponse, ABC):
  def __init__(self, logger, ssh, insert:dict, remove:dict, state:dict, vars:dict):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.sudo_password = None
    if 'sudo_password' in vars and vars['sudo_password'] != '':
      self.sudo_password = vars['sudo_password']
    self.ssh = ssh
    self.delta_insert = insert
    self.delta_remove = remove
    self.state = state

  def apply_insert(self):
    self.log.fn = self.__class__.__name__ + '.' + self.apply_insert.__name__
    state = {}
    for mod, names in self.delta_insert.items():
      state[mod] = {}
      cmd = MODS_COMMAND[mod]
      for name, param in names.items():
        self.log.info('{}'.format(ssh_command(cmd['insert'], param)))
        exec = ssh_command(cmd['insert'], param, self.sudo_password)
        if exec[:4] == "sudo":
          status, output = self.ssh.run(exec, self.sudo_password)
        else:
          status, output = self.ssh.run(exec, None)

        if status == 0:
          if not mod in self.state:
            self.state[mod] = {}
          self.state[mod][name] = param
          self.state[mod][name]['output'] = output
          self.log.info('{} : {}'.format(name, self.state[mod][name]))
        else:
          self.log.error('mod {} returned status code {}.'.format(mod, status))

  def apply_remove(self):
    self.log.fn = self.__class__.__name__ + '.' + self.apply_remove.__name__
    for mod, names in self.delta_remove.items():
      cmd = MODS_COMMAND[mod]
      for name in names.keys():
        if name in self.state[mod]:
          self.log.info('{}'.format(ssh_command(cmd['remove'], self.state[mod][name])))
          exec = ssh_command(cmd['remove'], self.state[mod][name], self.sudo_password)
          if exec[:4] == "sudo":
            status, output = self.ssh.run(exec, self.sudo_password)
          else:
            status, output = self.ssh.run(exec, None)

          if status == 0:
            self.log.info('{} : {}'.format(name, self.state[mod][name]))
            del self.state[mod][name]
          else:
            self.log.error('mod {} returned status code {}:{}.'.format(mod, status, output))
