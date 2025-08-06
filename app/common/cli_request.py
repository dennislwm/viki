from glob import glob
from pathlib import Path
import json, os, yaml

class CliRequest():
  def __init__(self, logger, path="."):
    self.log = logger
    self.log.fn = self.__class__.__name__ + '.' + self.__init__.__name__
    self.path = path
    self.state = self.__load_state(state={
      'viki': {
        'data': {},
        'mods': {}
      }
    })
    self.log.info("load state file complete.")
    self.config = self.__load_config(config={
      'viki': {
        'data': {},
        'vars': {},
        'mods': {}
      }
    })
    self.log.info("load config files complete.")
    self.vars = self.__load_os(self.config['vars'])
    self.mods = self.config['mods']
    self.data = self.config['data']
    self.state_mods = self.state['viki']['mods']

  def __load_state(self, state:dict, file="state.vk.json"):
    """Loads a state file
      :param file: A file name, defaults to state.vk.json
      :type file: string
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__load_state.__name__
    state_file = Path(self.path + '/' + file)
    if state_file.is_file():
      with open(self.path + '/' + file) as fp:
        state = json.load(fp)
      fp.close()
    return state

  def write_state(self, state:dict, file="state.vk.json"):
    """Writes a state file
      :param file: A file name, defaults to state.vk.json
      :type file: string
    """
    self.log.fn = self.__class__.__name__ + '.' + self.write_state.__name__
    with open(self.path + '/' + file, 'w') as fp:
      json.dump(state, fp, indent=2)
    fp.close()
    return state

  def __load_config(self, config:dict):
    """Loads one or more configuration files
    """
    self.log.fn = self.__class__.__name__ + '.' + self.__load_config.__name__
    viki = config['viki']
    paths = [Path(p) for p in glob(self.path + '/' + '*.vk.yaml')]
    for file in paths:
      with open(file) as fp:
        data = yaml.safe_load(fp)
        for conf, obj in viki.items():
          if conf in data['viki']:
            for key, val in data['viki'][conf].items():
              if not key in viki[conf]:
                viki[conf][key] = val
              else:
                self.log.error("Duplicate key {} found.".format(key), KeyError)
      fp.close()
    return viki

  def __load_env_file(self):
    """Load environment variables from .env file in the specified path"""
    env_file = os.path.join(self.path, '.env')
    if os.path.exists(env_file):
      try:
        with open(env_file, 'r') as f:
          for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
              # Handle 'export KEY=value' format
              if line.startswith('export '):
                line = line[7:]  # Remove 'export ' prefix
              
              key, value = line.split('=', 1)
              key = key.strip()
              value = value.strip().strip('"\'')  # Remove quotes
              
              # Handle variable expansion like ${VK_VAR_password}
              if value.startswith('${') and value.endswith('}'):
                ref_var = value[2:-1]  # Remove ${ and }
                value = os.environ.get(ref_var, value)  # Use referenced value or keep original
              
              os.environ[key] = value
      except Exception:
        pass  # Fail silently if .env file cannot be read

  def __load_os(self, vars:dict) -> dict:
    self.log.fn = self.__class__.__name__ + '.' + self.__load_os.__name__
    # Load .env file first
    self.__load_env_file()

    for key, val in os.environ.items():
      if key[:7] == 'VK_VAR_':
        var = key[7:]
        if var in vars:
          vars[var] = val
    return vars

  def approval(self) -> bool:
    user_input = input("Do you want to perform these actions?  \nviki will perform the actions described above.\n  Only 'yes' will be accepted to approve.\n\n  Enter a value: ")
    if user_input.lower() == 'yes':
      return True
    return False