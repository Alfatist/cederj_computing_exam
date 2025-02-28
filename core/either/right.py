from .either import Either


class Right(Either):
  '''Represents a success.'''
  code:int
  result: any
  def __init__(self, result, code:str = -1): self.code, self.result = code, result