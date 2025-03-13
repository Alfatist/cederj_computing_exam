import json
import os

from core.either.either import Either
from core.either.left import Left
from core.either.right import Right

def writeEndpointJson(fileName:str, write) -> Either:
  try:
    newJson = json.dumps(write)
    pathJson = os.path.join(os.getcwd(), "core/assets", fileName)
    open(pathJson, "w").write(newJson)
    return Right("Successfully wrote.")
  except Exception as e:
    return Left(ConnectionError, 5)