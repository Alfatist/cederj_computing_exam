import sys
import os

from usecases.addAccountToUserJsonRepository import addAccountToUserJsonRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs
from usecases.addToYieldRepository import addToYieldJsonRepository


def createSavingAccountJsonRepository(holderName, address, agency = "0001") -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    if(type(accounts) == Left): return accounts
    accountID = accounts["nextId"]
    accounts["nextId"] = accountID + 1
    newJson = accounts["defaultSavingAccountDict"].copy()
    newJson["holderName"] = holderName
    newJson["holderAddress"] = address
    newJson["agency"] = agency
    accountID = str(accountID)
    
    accounts[accountID] = newJson
    either = writeEndpointJson(AppURLs.accounts, accounts)
    result = addToYieldJsonRepository(accountID, 0)
    if(type(result) == Left): raise result.result
    if(type(either) == Right): 
      addAccountToUserJsonRepository(holderName, accountID)
      return Right(accountID)
    return Left(ConnectionError, 5)
  except Exception as e:
    raise e
    return Left(Exception)