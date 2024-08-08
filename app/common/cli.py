import argparse

class Cli:
  def __init__(self, app:str, desc:str):
    self.parser = argparse.ArgumentParser(
      prog= app,
      description=desc)
    self.subparser = self.parser.add_subparsers(dest='command')
    self.subparser.required = True
    self.__add_option_path()
    self.__add_command_fetch()
    self.__add_command_plan()
    self.__add_command_apply()

  def __add_option_path(self):
    self.parser.add_argument(
      '-p',
      '--path',
      type=str,
      default='.',
      help='path to the configuration and state files'
    )

  def __add_command_fetch(self):
    self.subparser.add_parser(
      'fetch',
      help='fetch data resources into state file'
    )

  def __add_command_plan(self):
    self.subparser.add_parser(
      'plan',
      help='create a plan from configuration files'
    )

  def __add_command_apply(self):
    self.subparser.add_parser(
      'apply',
      help='applies a plan from configuration files'
    )

  def args(self):
    return self.parser.parse_args()