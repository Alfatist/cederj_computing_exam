import sys
import os
import datetime

from usecases.addToStatementJsonRepository import addToStatementJsonRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def addMoneyToBalanceAccountJsonRepository(account:str, number:float, toIncludeStatement = True) -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    accounts[account]["balance"] += number
    if(toIncludeStatement): addToStatementJsonRepository(account, f"Depósito de {number} reais")
    return writeEndpointJson(AppURLs.accounts, accounts)
  except: return Left("Erro desconhecido.")
  
def getBalanceAccountJsonRepository(account) -> float: return float(getEndpointJson(AppURLs.accounts)[account]["balance"])
  
def getAddressAccountJsonRepository(account) -> str: return getEndpointJson(AppURLs.accounts)[account]["holderAddress"]

def checkIfAccountExistJsonRepository(account) -> bool:
  try:
    if(getEndpointJson(AppURLs.accounts).get(account) != None): return True
    return False
  except: return False

def transferMoneyAccountJsonRepository(accountTransfering, accountToTransfer, value):
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    fromAccount, toAccount = accounts[accountTransfering], accounts[accountToTransfer]
    fromAccount["balance"] -= value
    toAccount["balance"] += value
    accounts[accountTransfering], accounts[accountToTransfer] = fromAccount, toAccount
    
    addToStatementJsonRepository(accountTransfering ,f"Transferência de {value} reais para a conta de id {accountToTransfer}")
    addToStatementJsonRepository(accountToTransfer ,f"Transferência de {value} reais vindo da conta de id {accountTransfering}")

    return writeEndpointJson(AppURLs.accounts, accounts)
  except:
    return Left("Erro desconhecido")


def changeHolderAddressJsonRepository(account, newAddress) -> Either:
  try:
    newJson = getEndpointJson(AppURLs.accounts)
    newJson[account]["holderAddress"] = newAddress
    return writeEndpointJson(AppURLs.accounts, newJson)
  except:
    return Left("Erro desconhecido")
