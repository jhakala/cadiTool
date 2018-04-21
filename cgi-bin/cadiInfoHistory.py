import sqlite3
import json
import json_delta
from copy import deepcopy
from datetime import datetime, timedelta
from cadiInfoRenderer import printInfo, selectAnalyses
from cadiDeltaLogger import connectToDB

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getCadiInfo():
  dbConn = connectToDB('/afs/cern.ch/user/j/johakala/www/pw/cadiTool/cadiDiffs.sqlite')
  cadiCacheName = '/afs/cern.ch/user/j/johakala/www/pw/cadiTool/cadiCache.json' # TODO: make this name shared between cadiDeltaLogger and here
  cachedJson = deepcopy(json.load(open(cadiCacheName)))
  return (dbConn, cachedJson)

def decodePatch(patch):
  pass

def getHistoricalCadiInfo(pastTimestamp):
  messages = ""
  dbConn, cadiInfo = getCadiInfo()
  for row in dbConn.execute("SELECT diffStanza FROM deltas WHERE timestamp BETWEEN ? AND ?", (pastTimestamp, datetime.utcnow())):
    messages += str(row) + "\n"
    for stanza in row:
      patch_stanza = json.loads(stanza.decode('utf-8'))
      messages += str(patch_stanza) + ", "
      json_delta._patch.patch_stanza(cadiInfo, patch_stanza)
      
  return (messages, cadiInfo)

if __name__ == "__main__":
  cadiInfo = getCadiInfo()[1]
  print "type(cadiInfo)"
  print type(cadiInfo)
  messages, historicalCadiInfo = getHistoricalCadiInfo(datetime.utcnow() - timedelta(minutes=60*24))
  print messages
  print "type(historicalCadiInfo)"
  print type(historicalCadiInfo)
  printInfo(selectAnalyses(cadiInfo, ["HIN-18-006"]))
  printInfo(selectAnalyses(historicalCadiInfo, ["HIN-18-006"]))
  printInfo(cadiInfo)
  printInfo(historicalCadiInfo)
