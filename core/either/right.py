from .either import Either


class Right(Either):
  '''Represents a success.'''
  message:str
  result: any
  def __init__(self, message:str, result = -1): self.message, self.result = message.strip(), result