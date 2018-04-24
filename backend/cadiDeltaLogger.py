import requests
import cookielib
import json
import json_delta
import sqlite3
import shlex
from time import sleep
from datetime import datetime
from os import path, getcwd, remove, environ
from subprocess import check_call


def connectToDB(dbFileName = "cadiDiffs.sqlite"):
  # setup for reading what's in the cadi diffs database
  conn = sqlite3.connect(dbFileName, detect_types=sqlite3.PARSE_DECLTYPES) 
  return conn

def initializeDB(conn):
  # create the database that stores the log of "deltas" in the cadi json
  # these deltas allow us to retrace the history of what changed in cadi
  # this method should only be run ONCE EVER!
  conn.execute("CREATE TABLE deltas (id integer primary key, diffStanza text, [timestamp] timestamp)")
  print "database initialized."
  
def insertDelta(conn, diffStanza):
  # insert a record of what has changed into the local sqlite database file
  conn.execute("INSERT INTO deltas(diffStanza, timestamp) values (?, ?)", (diffStanza, datetime.utcnow()))
  conn.commit() 


def getCadiJson():
  # gets the json from the cadi API
  ## get cookie
  cookieFileName = "cadiana.sso"
  cookieFile = path.join(getcwd(), cookieFileName)
  check_call(shlex.split("/usr/bin/cern-get-sso-cookie -u https://icms.cern.ch/tools/api/cadiAnalyses --krb --outfile {0} --reprocess".format(cookieFileName)))
  ## setup for stuff needed to submit the http request with a cookie
  apiURL = "https://icms.cern.ch/tools/api/cadiAnalyses"
  ## parsing of the cookie
  cjar = cookielib.MozillaCookieJar(cookieFile, None, None)
  cjar.load()
  ## setting up to query the cadi API
  session = requests.Session()
  ## use the cookie
  session.cookies = cjar
  ## return the info into json form
  return session.post(apiURL, verify=False).json()

def getFakeCadiJson():
  return requests.get('https://johakala.web.cern.ch/johakala/dummy.json').json()

if __name__ == "__main__":
  #### DEBUG MODE FLAG ####
  debugMode = True # for debugging

  connectedToDB = False
  # prompt the user if they _really_ want to recreate the database
  from sys import argv
  if len(argv) == 2:
    if argv[1] == "initDB":
      while True:
        choice = raw_input("initialize the database?\n").lower()
        if choice == "y":
          if path.exists(dbFileName):
            remove(dbFileName) 
          conn = connectToDB()
          connectedToDB = True
          initializeDB(conn)
          break
        elif choice == "n":
           print "aborting!"
           exit(1)
        else:
           print "Please respond with 'y' or 'n'\n"
    else:
      print "invalid argument supplied, only 'initDB' is allowed"
      exit(1)
  elif len(argv) > 2:
    print "invalid number of arguments"
    exit(1)

  if not connectedToDB:
    conn = connectToDB()

  # now proceed to monitor the JSON from the API
  ## initialize the cache
  ## we read it from a local json file that stores what this program
  ## last saw when it was running last
  cadiCacheName = 'cadiCache.json'
  cachedJson = json.load(open(cadiCacheName))
  
  ## every two seconds, check for a diff of the json
  cookieFileName = "cadiana.sso"
  cookieFile = path.join(getcwd(), cookieFileName)
  check_call(shlex.split("/usr/bin/cern-get-sso-cookie -u https://icms.cern.ch/tools/api/cadiAnalyses --krb --outfile {0} --reprocess".format(cookieFileName)))
  while True:
    if debugMode:
      print "querying CADI api"
    #currentJson = getCadiJson() if not debugMode else getFakeCadiJson()
    currentJson = getCadiJson() 
    if debugMode:
      print "diffing retrieved json from CADI api"
    diff = json_delta._diff.diff(currentJson, cachedJson, False, False, 0.0, False)
    if len(diff)>0:
      if debugMode :
        print diff
      # put the diff into the sqlite database of all diffs
      # this makes sure to put the stanza's text in valid json format
      for stanza in diff:
        insertDelta(conn, json.dumps(stanza))
    elif debugMode:
      print "no changes to cadi API json found"
      
    cachedJson = currentJson 
    # in case this program stops, save the cadi json to a local file so that
    # if anything changed in cadi between the last time this program ran and the current run
    # then 'diffs' corresponding to those changes can be reconstructed
    with open(cadiCacheName, 'w') as outfile:
      json.dump(cachedJson, outfile)
    outfile.close()
    sleep(2)
