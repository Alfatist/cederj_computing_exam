import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.removeMoneyFromBalanceAccountJsonRepository import removeMoneyFromBalanceAccountJsonRepository
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from usecases.addToYieldRepository import addToYieldJsonRepository
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs 

def addMoneyToBalanceAccountJsonRepository(account:str, number:float, isToIncludeStatement = True, isToIncludeYield = True) -> Either:
  '''add or remove money to account balance. Also include in statement and yield if needed'''
  try:
    if(number == 0): return Left(ValueError, 7)
    if(number < 0): return removeMoneyFromBalanceAccountJsonRepository(account, -number, isToIncludeStatement)
  
    accounts = getEndpointJson(AppURLs.accounts)
    if(type(accounts) == Left): return accounts

    accounts[account]["balance"] += number
    if(accounts[account]["type"] == "Conta Poupança" and isToIncludeYield): addToYieldJsonRepository(account, number)
    if(isToIncludeStatement): 
      resultAddToStatement = addToStatementJsonRepository(account, f"Depósito de {number} reais")
      if(type(resultAddToStatement) == Left): return resultAddToStatement
  
    return writeEndpointJson(AppURLs.accounts, accounts)
  except Exception as e: return Left(e)