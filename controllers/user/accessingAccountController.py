from core.either.left import Left
from updates.getStatementOfAccountJsonRepository import getStatementOfAccountJsonRepository
from updates.accessingAccountJsonRepository import addMoneyToBalanceAccountJsonRepository, changeHolderAddressJsonRepository, checkIfAccountExistJsonRepository, getAddressAccountJsonRepository, getBalanceAccountJsonRepository, transferMoneyAccountJsonRepository
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
    if(not accountToCheck.isnumeric()): return False
    return checkIfAccountExistJsonRepository(accountToCheck)
  
  def transferMoneyToAccount(self, accountToTransfer:str, value: float) -> Either:
    if(0 < value < self.getBalance() and accountToTransfer.isnumeric()): return transferMoneyAccountJsonRepository(self.__accountId, accountToTransfer, value)
    return Left("Valor inválido.")
  
  def getStatementOfAccount(self) -> str:
    statementResponse = getStatementOfAccountJsonRepository(self.__accountId)
    responseType = type(statementResponse)
    if(responseType == Right):
      jsonStatementAccount = statementResponse.result
      if (jsonStatementAccount == None or jsonStatementAccount == {}): return "Não há extrato para esta conta."
      fullStatementToString = ""
      dates = list(jsonStatementAccount.keys())
      for date in dates:
        fullStatementToString += f"{date}:\n\n"
        fullStatementToString += f"{"\n".join(jsonStatementAccount[date])}\n\n"
      return fullStatementToString
    return "Desculpe, tivemos um erro ao tentar pegar o extrato."
    
  def changeHolderAddress(self, newAddress):
    return changeHolderAddressJsonRepository(self.__accountId, newAddress)
