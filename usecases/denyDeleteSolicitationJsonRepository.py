import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def denyDeleteSolicitationJsonRepository(idAccount) -> Either:
  try:
    solicitations = getEndpointJson(AppURLs.deleteSolicitations)
    if(type(solicitations) == Left): return solicitations
    
    solicitations.pop(idAccount)
    return writeEndpointJson(AppURLs.deleteSolicitations, solicitations)
  except Exception as e:
    return Left(e)
