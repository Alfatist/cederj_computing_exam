from .either import Either

codeErrorsMessages = { 
  0: "Unknown error",
  1: "Login not found",  
  2: "Password wrong",
  3: "Account already exist",
  4: "Password weak. Minimum 8 characters"
}

class Left(Either):
  '''Represents a failure. Should be treated'''
  message:str
  result:str

  def __init__(self, message:str, code = 0): 
    self.message = message + f"\nCode {code}: {codeErrorsMessages[code]}"
    self.result = code
    self.message = self.message.strip()
  
  def __str__(self): return self.message