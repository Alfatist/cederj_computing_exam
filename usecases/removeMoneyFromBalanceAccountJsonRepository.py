import sys
import os

from usecases.removeMoneyFromSpecialCheckJsonrepository import removeMoneyFromSpecialCheckJsonrepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from usecases.getAvailableCheckJsonRepository import getAvailableCheckJsonRepository
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs
  

def removeMoneyFromBalanceAccountJsonRepository(account:str, number:float, isToIncludeStatement = True) -> Either:
  '''remove money from account balance. Also include in statement if needed. Can be negative.'''
  if(number == 0): return Left(ValueError, 7)
  if(number < 0): number = -number
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    if(type(accounts) == Left): return accounts

    modifiedBalance = accounts[account]["balance"] - number
    
    if(accounts[account]["type"] == "Conta Poupança"): 
      if(modifiedBalance < 0): return Left(ValueError, 8)

    elif(accounts[account]["type"] == "Conta Corrente" and modifiedBalance < 0 ): 
      valueMissingNegative = modifiedBalance
      modifiedBalance -= valueMissingNegative
      valueAvailableSpecialCheck = getAvailableCheckJsonRepository(account)
      if(type(valueAvailableSpecialCheck) == Left): return valueAvailableSpecialCheck
      if(valueAvailableSpecialCheck + valueMissingNegative < 0): return Left(ValueError, 9)
      resultRemoveMoney = removeMoneyFromSpecialCheckJsonrepository(account, valueMissingNegative)
      if(type(resultRemoveMoney) == Left): return resultRemoveMoney

    accounts[account]["balance"] = modifiedBalance
    if(isToIncludeStatement): 
      addedToStatement = addToStatementJsonRepository(account, f"Saque de {number} reais")
      if(type(addedToStatement) == Left): return addedToStatement
  
    return writeEndpointJson(AppURLs.accounts, accounts)
  
  except Exception as e: return Left(e) 