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
    resultClient = getEndpointJson(AppURLs.clients)
    resultSolicitations = getEndpointJson(AppURLs.deleteSolicitations)

    resultClient[holderName].remove(int(account))
    resultSolicitations.pop(account)

    writeEndpointJson(AppURLs.clients, resultClient)
    return writeEndpointJson(AppURLs.deleteSolicitations, resultSolicitations)
  except Exception as e:
    return Left(e)
