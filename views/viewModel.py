class ViewModel:
  exitValue = "0"
  isToLeave:bool


  def __init__(self, argument):
    self.isToLeave = False

  def call(self):
    raise NotImplementedError

  def inputView(self, message:str):
    if(not self.isToLeave): 
      valueInput = input(message)
      if(valueInput == self.exitValue): self.isToLeave = True
      return valueInput
  
  def pressAnyKeyToContinue(self):
    '''Function to wait a userInput to continue'''
    self.inputView(f"\nPressione qualquer tecla para continuar, ou {self.exitValue} para sair: ")

  def returnView(self, returnExpected:list):
    '''or return None (to exit all), or return a list with 2 Items. Index 0 with keycode to main, and index 1 with arguments'''
    if(self.isToLeave): return None
    if(type(returnExpected) == list): return returnExpected
    return returnExpected()