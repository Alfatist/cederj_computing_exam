from core.either.either import Either
from core.either.left import Left
from core.either.right import Right
from usecases.getAccountJsonRepository import getAccountJsonRepository
from usecases.deleteAccountJsonRepository import deleteAccountJsonRepository
from usecases.denyDeleteSolicitationJsonRepository import denyDeleteSolicitationJsonRepository
from usecases.getDeleteSolicitationsJsonRepository import getDeleteSolicitationsJsonRepository


class ConfirmDeleteAccountsController(object):

  deleteSolicitations: dict

  def getAccount(self, value) -> Left | dict:
    return getAccountJsonRepository(value)
    
  
  def getDeleteSolicitations(self) -> Left | dict: 
    result = getDeleteSolicitationsJsonRepository()
    if(type(result) == dict): self.deleteSolicitations = result
    return result
  
  def deleteAccount(self, holderName, idAccount) -> Either: return deleteAccountJsonRepository(holderName, idAccount)
  
  def denyDeleteAccount(self, idAccount) -> Either: return denyDeleteSolicitationJsonRepository(idAccount)
  