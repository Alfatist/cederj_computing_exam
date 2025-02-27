import sys
import os

from model.crudAccountToUserJsonRepository import addAccountToUser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def CreateCurrentAccountJsonRepository(holderName) -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    accountID = accounts["nextId"]
    accounts["nextId"] = accountID + 1
    accounts[accountID] = accounts["defaultCurrentAccountDict"]
    either = writeEndpointJson(AppURLs.accounts, accounts)
    if(type(either) == Right): return addAccountToUser(holderName, accountID)
    return Left("Não foi possível criar a nova conta.", 5)
  except:
    return Left("Erro desconhecido.")
  
def CreateSavingAccountJsonRepository(holderName) -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    accountID = accounts["nextId"]
    accounts["nextId"] = accountID + 1
    accounts[accountID] = accounts["defaultSavingAccountDict"]
    either = writeEndpointJson(AppURLs.accounts, accounts)
    if(type(either) == Right): return addAccountToUser(holderName, accountID)
    return Left("Não foi possível criar a nova conta.", 5)
  except:
    return Left("Erro desconhecido.")


# testes 
# print(CreateUserJsonRepository("mateus", "123456789").message) # should return an account exist
# print(CreateUserJsonRepository("Mateus", "123456789").message) # should rewrite the json
# print(CreateUserJsonRepository("mateus", "123456789").message) # should rewrite the json