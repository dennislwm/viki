import logging, sys

class Logger:
  def __init__(self, fn:str, id:int=0, level=logging.INFO):
    self.id = id
    self.fn = fn
    self.log = logging.getLogger()
    self.log.setLevel(level)
    if self.fn == "__main__":
      handler = logging.StreamHandler(sys.stdout)
      self.log.addHandler(handler)

  def info(self, msg):
    self.log.info('[cid:{}][INFO][{}] {}'.format(self.id, self.fn, msg))

  def warning(self, msg):
    self.log.warning('[cid:{}][WARNING][{}] {}'.format(self.id, self.fn, msg))

  def error(self, msg, e=None):
    self.log.error('[cid:{}][ERROR][{}] {}'.format(self.id, self.fn, msg))
    if not e is None:
      if type(e) is KeyError:
        raise Exception('[cid:{}][ERROR][{}] {} is missing from dict.'.format(self.id, self.fn, str(e)))
      else:
        raise Exception('[cid:{}][ERROR][{}] {}'.format(self.id, self.fn, str(e)))