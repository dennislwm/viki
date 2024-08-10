DATA_COMMAND={
  "df": "df -h",
  "docker": "sudo docker ps",
  "ls": "ls ${path}",
  "lsl": "ls -lAG ${path}"
}

MODS_COMMAND={
  "mkdir": {
    "insert": "sudo mkdir -p ${path}",
    "remove": "sudo rmdir ${path}"
  },
  "wget": {
    "insert": "wget -O ${path}/${output} ${url}",
    "remove": "rm ${path}/${output}"
  }
}

def ssh_command(command: str, config_param: dict, sudo_password: str = None) -> str:
  '''
  Replace placeholders in ssh command with configuration parameters.

  Here is an example of a command, config_param and return value:

    command             "ls -lAG ${path}"
    config_param        { "path" : "~" }
    returns             "ls -lAG ~"

  @param command        The command with placeholders to substitute.
  @param config_param   The configuration parameters.
  @param sudo_password  Used for sudo password authentication. (Default: None for passwordless)
  @returns              The ssh command to run with actual values.
  '''
  ret = command
  if ret[:4] == "sudo" and not sudo_password is None:
    if len(sudo_password)>0:
      ret = "echo " + sudo_password + " | " + ret[:4] + " -S " + ret[5:]
  for key, val in config_param.items():
    sub = '${' + key + '}'
    ret = ret.replace(sub, val)
  return ret