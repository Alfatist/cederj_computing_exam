from core.either.left import Left
from model.accessingAccountJsonRepository import addMoneyToBalanceAccountJsonRepository, checkIfAccountExistJsonRepository, getAddressAccountJsonRepository, getBalanceAccountJsonRepository, transferMoneyAccountJsonRepository
from core.either.either import Either
from core.either.right import Right




class AccessingAccountController(object):
  __holderName:str
  __accountId:str
  def __init__(self, name:str, accountId:str): self.__name, self.__accountId = name, accountId

  def getName(self): return self.__name
  def getAccountId(self): return self.__accountId

  def addMoney(self, number: float) -> Either:
    if(number < 0): return Left("Valor inválido")
    return addMoneyToBalanceAccountJsonRepository(self.__accountId, number)

  def getBalance(self) -> float: return getBalanceAccountJsonRepository(self.__accountId)
  
  def getAddress(self) -> Either: return getAddressAccountJsonRepository(self.__accountId)
  
  def checkAccountExist(self, accountToCheck:str) -> bool: 
    if(not accountToCheck.isnumeric): return False
    return checkIfAccountExistJsonRepository(accountToCheck)
  
  def transferMoneyToAccount(self, accountToTransfer:str, value: float) -> Either:
    if(0 < value < self.getBalance() and accountToTransfer.isnumeric()): return transferMoneyAccountJsonRepository(self.__accountId, accountToTransfer, value)
    return Left("Valor inválido.")