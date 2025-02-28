from .either import Either

codeErrorsMessages = { 
  0: "Unknown error",
  1: "Login not found",  
  2: "Password wrong",
  3: "Account already exist",
  4: "Password weak. Minimum 8 characters",
  5: "Error while trying to write in json"
}

class Left(Either):
  '''Represents a failure. Should be treated'''
  code:str
  result:str

  def __init__(self, result:any, code = 0): 
    self.code = code
    self.result = result
    
  
  def __str__(self): return f"{self.code}: {codeErrorsMessages[self.code]}"