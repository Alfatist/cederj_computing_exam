import sys
import os

from updates.crudAccountToUserJsonRepository import addAccountToUserJsonRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def CreateCurrentAccountJsonRepository(holderName, address, agency = "0001") -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    accountID = accounts["nextId"]
    accounts["nextId"] = accountID + 1
    newJson = accounts["defaultCurrentAccountDict"]
    newJson["holderName"] = holderName
    newJson["holderAddress"] = address
    newJson["agency"] = agency
    
    accounts[accountID] = newJson
    either = writeEndpointJson(AppURLs.accounts, accounts)
    if(type(either) == Right): return addAccountToUserJsonRepository(holderName, accountID)
    return Left("Não foi possível criar a nova conta.", 5)
  except:
    return Left("Erro desconhecido.")
  
def CreateSavingAccountJsonRepository(holderName, address, agency = "0001") -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    accountID = accounts["nextId"]
    accounts["nextId"] = accountID + 1
    newJson = accounts["defaultSavingAccountDict"]
    newJson["holderName"] = holderName
    newJson["holderAddress"] = address
    newJson["agency"] = agency
    
    accounts[accountID] = newJson
    either = writeEndpointJson(AppURLs.accounts, accounts)
    if(type(either) == Right): return addAccountToUserJsonRepository(holderName, accountID)
    return Left("Não foi possível criar a nova conta.", 5)
  except:
    return Left("Erro desconhecido.")