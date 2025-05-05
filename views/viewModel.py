import tkinter as tk
from tkinter import messagebox

class ViewModel:
  exitValue = "0"
  isToLeave:bool


  def __init__(self, argument = ""):
    self.isToLeave = False
    self.result = None
    self.values = None
    self.root = None
    if(self.root != None and len(self.root.children) != 0): self.root.destroy()


  def call(self):
    raise NotImplementedError

  def inputView(self, message:str = ""):
    self.values = None
    self.root = tk.Tk()
    self.root.title("CEDERJ BANK")
    tk.Label(self.root, text=message, font=("Arial", 12), ).pack(pady=10)
    self.value = tk.Entry(self.root)
    self.value.pack(padx=5)
    self.login_button = tk.Button(self.root, text="Submeter", command=lambda: self.returnDestroy(self.value.get()))
    self.login_button.pack(pady=10)
    self.root.mainloop()
    return self.values
  
  def pressAnyKeyToContinue(self):
    '''Function to wait a user input to continue'''
    self.inputView(f"\nPressione qualquer tecla para continuar, ou {self.exitValue} para sair: ")

  def returnView(self, returnExpected:list) -> list | None:
    '''or return None (to exit all), or return a list with 2 Items. Index 0 with keycode to main, and index 1 with arguments'''
    if(self.isToLeave): return None
    if(type(returnExpected) == list): return returnExpected
    return returnExpected()
  
  def setResult(self, value): 
    if(len(self.root.children) != 0): self.root.destroy()
    self.result = value
  
  def returnDestroy(self, values):
    self.values = values
    self.root.destroy()

  def print(self, message:str):
    messagebox.showinfo("Informação", message)