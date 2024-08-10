from common.cli_request import CliRequest
from common.logger import Logger
from common.cli import Cli
from common.my_ssh import MySSH
from common.fetch_response import FetchResponse
from common.plan_response import PlanResponse
from common.apply_response import ApplyResponse
import sys

# ================================================================
# MAIN
# ================================================================
def main():
  logger = Logger(__name__)
  cli = Cli(
    app='viki',
    desc='CLI application that manages servers using a declarative configuration'
  )
  request = CliRequest(logger, path=cli.args().path)
  logger.fn = __name__
  if not 'hostname' in request.vars or not 'username' in request.vars or not 'password' in request.vars or request.vars['hostname'] == '' or request.vars['username'] == '' or request.vars['password'] == '':
    logger.error('SSH credentials not found.')
    sys.exit(1)

  # Create the SSH connection
  ssh = MySSH()
  ssh.set_verbosity(False)
  ssh.connect(
    hostname=request.vars['hostname'],
    username=request.vars['username'],
    password=request.vars['password'],
    port=22
  )
  if ssh.connected() is False:
    logger.error('SSH connection failed.')
    sys.exit(1)

  if cli.args().command == 'fetch':
    fetch_response = FetchResponse(logger, ssh, request.data, request.vars)
    fetch_response.fetch()
    request.state['viki']['data'] = fetch_response.state
    request.write_state(request.state)
  elif cli.args().command == 'plan' or cli.args().command == 'apply':
    plan_response = PlanResponse(logger, ssh, request.mods, request.state_mods)
    logger.fn = __name__
    if plan_response.count_insert == 0 and plan_response.count_remove == 0:
      logger.info('No changes. Your server matches the configuration.')
    else:
      if plan_response.count_insert > 0:
        logger.info('add:\n{}'.format(plan_response.pretty_json(plan_response.delta_insert)))
      if plan_response.count_remove > 0:
        logger.info('destroy:\n{}'.format(plan_response.pretty_json(plan_response.delta_remove)))
      logger.info('Plan {} to add, {} to destroy.'.format(plan_response.count_insert, plan_response.count_remove))
      if cli.args().command == 'apply':
        fetch_response = FetchResponse(logger, ssh, request.data, request.vars)
        fetch_response.fetch()
        request.state['viki']['data'] = fetch_response.state
        apply_response = ApplyResponse(logger, ssh, plan_response.delta_insert, plan_response.delta_remove, request.state_mods, request.vars)
        if request.approval():
          if plan_response.count_insert > 0: apply_response.apply_insert()
          if plan_response.count_remove > 0: apply_response.apply_remove()
          request.state['viki']['mods'] = apply_response.state
          request.write_state(request.state)
          logger.info('Apply complete! {} added, {} destroyed.'.format(plan_response.count_insert, plan_response.count_remove))

if __name__ == "__main__":
  main()
