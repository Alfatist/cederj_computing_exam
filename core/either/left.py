from .either import Either

codeErrorsMessages = { 
  0: "Unknown error",
  1: "Login not found",  
  2: "Password wrong",
  3: "Account already exist",
  4: "Password weak. Minimum 8 characters",
  5: "Error while trying to write in json",
  6: "Error can't get json",
  7: "Value less or equal to 0",
  8: "Balance saving can't be less than 0",
  9: "Balance and SpecialCheck not enough",
  10: "Check Special not found",
  11: "Balance is equal to 0",
  12: "invalid value",
  13: "Check Special used is 0"
}

class Left(Either):
  '''Represents a failure. Should be treated'''
  code:str
  result:any

  def __init__(self, result:any, code = 0): 
    self.code = code
    self.result = result
    
  
  def __str__(self): return f"{self.code}: {codeErrorsMessages[self.code]}"