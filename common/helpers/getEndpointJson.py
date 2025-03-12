import json
import os

from core.either.left import Left

def getEndpointJson(fileName:str) -> Left | dict:
  try:
    pathJson = os.path.join(os.getcwd(), "core/assets", fileName)
    file = open(pathJson, "r")
    return json.load(file)
  except Exception as e:
    return Left(e, 6)