import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def deleteAccountJsonRepository(holderName, account) -> Either:
  try:
    account = str(account)
    resultClient = getEndpointJson(AppURLs.clients)
    if(type(resultClient) == Left): return resultClient
    resultSolicitations = getEndpointJson(AppURLs.deleteSolicitations)
    if(type(resultSolicitations) == Left): return resultSolicitations
    
    resultClient[holderName].remove(account)
    resultSolicitations.pop(account)

    resultWriting = writeEndpointJson(AppURLs.clients, resultClient)
    if(type(resultWriting) == Left): return resultWriting
    return writeEndpointJson(AppURLs.deleteSolicitations, resultSolicitations)
  except Exception as e: return Left(e)
