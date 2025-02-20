import json
import os

def getEndpointJson(fileName:str) -> dict:
  pathJson = os.path.join(os.getcwd(), "core/assets", fileName)
  file = open(pathJson, "r")
  return json.load(file)