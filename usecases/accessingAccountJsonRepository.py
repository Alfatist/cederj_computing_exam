import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.removeMoneyFromBalanceAccountJsonRepository import removeMoneyFromBalanceAccountJsonRepository
from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from usecases.addMoneyToSpecialCheckJsonrepository import addMoneyToSpecialCheckJsonrepository 
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from usecases.addToYieldRepository import addToYieldJsonRepository
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs
  

def addMoneyToBalanceAccountJsonRepository(account:str, number:float, isToIncludeStatement = True, isToIncludeYield = True) -> Either:
  '''add or remove money to account balance. Also include in statement and yield if needed'''
  try:
    if(number == 0): return Left(ValueError, 7)
    if(number < 0): return removeMoneyFromBalanceAccountJsonRepository(account, -number, isToIncludeStatement)
  
    accounts = getEndpointJson(AppURLs.accounts)

    accounts[account]["balance"] += number
    if(accounts[account]["type"] == "Conta Poupança" and isToIncludeYield): addToYieldJsonRepository(account, number)
    if(isToIncludeStatement): addToStatementJsonRepository(account, f"Depósito de {number} reais")
  
    return writeEndpointJson(AppURLs.accounts, accounts)
  except Exception as e:
    return Left(e) 

  
def getBalanceAccountJsonRepository(account) -> float: return float(getEndpointJson(AppURLs.accounts)[account]["balance"])
  
def getAddressAccountJsonRepository(account) -> str: return getEndpointJson(AppURLs.accounts)[account]["holderAddress"]

def checkIfAccountExistJsonRepository(account) -> bool:
  try:
    accountsJson = getEndpointJson(AppURLs.accounts)
    accountName = accountsJson[account].get("holderName")
    accountIsOwnedByName = account in getEndpointJson(AppURLs.clients)[accountName] 
    
    if(accountsJson.get(account) != None and accountIsOwnedByName): return True
    return False
  except: return False

def transferMoneyAccountJsonRepository(accountTransfering, accountToTransfer, value):
  try:
    addMoneyToBalanceAccountJsonRepository(accountTransfering, -value, False)
    addMoneyToBalanceAccountJsonRepository(accountToTransfer, value, False)
    
    addToStatementJsonRepository(accountTransfering ,f"Transferência de {value} reais para a conta de id {accountToTransfer}")
    addToStatementJsonRepository(accountToTransfer ,f"Transferência de {value} reais vindo da conta de id {accountTransfering}")

    return Right("Transferência realizada com sucesso")
    
  except Exception as e:
    return Left(e)


def changeHolderAddressJsonRepository(account, newAddress) -> Either:
  try:
    newJson = getEndpointJson(AppURLs.accounts)
    newJson[account]["holderAddress"] = newAddress
    return writeEndpointJson(AppURLs.accounts, newJson)
  except Exception as e:
    return Left(e)
