exitValue = "0"

class ViewModel:
  isToLeave:bool


  def __init__(self):
    self.leave = False

  def inputView(self, message:str):
    if(not self.isToLeave): 
      valueInput = input(message)
      if(valueInput == exitValue): self.isToLeave = True
      return valueInput
  

  def returnView(self, returnExpected:list):
    '''or return None (to exit all), or return a list with 2 Items. Index 0 with keycode to main, and index 1 with arguments'''
    if(self.isToLeave): return None
    return returnExpected