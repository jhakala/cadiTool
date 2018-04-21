#!/opt/rh/python27/root/usr/bin/python

from datetime import datetime, timedelta

import cgi
import cgitb; cgitb.enable() # for troubleshooting

from cadiInfoHistory import *
from cadiInfoRenderer import htmlDiffInfo, htmlShowInfo, selectAnalyses, selectPhysWG
from cadiToolHtml import servePage

form = cgi.FieldStorage()
hoursAgo = int(form.getvalue('pastHours'))
wgFilters = []
analysisFilters = []
for key in form.keys():
  if key == "physWG":
    for physWG in form.getlist(key):
      wgFilters.append(physWG)
  if key == "analysis":
    for analysis in form.getlist(key):
      analysisFilters.append(analysis)
    

# get the full cadi infos from now and in the past
cadiInfoCurrent = getCadiInfo()[1]
(messages, cadiInfoPast) = getHistoricalCadiInfo(datetime.utcnow() - timedelta(minutes=60*hoursAgo))


# apply the filters the user requested
cadiInfoCurrent, codesCurrent = selectPhysWG(cadiInfoCurrent, wgFilters)
cadiInfoPast, codesPast = selectPhysWG(cadiInfoPast, wgFilters)
for code in codesCurrent:
  if not code in codesPast:
    cadiInfoPast.append({u"code":code, u"physWG":u''})
#for analysis in selectAnalyses(cadiInfoCurrent, analysisFilters):
#  cadiInfoCurrent.append(analysis)
#for analysis in selectAnalyses(cadiInfoPast, analysisFilters):
#  cadiInfoPast.append(analysis)

body = ""
#body += str(codesCurrent) + "<br>"
#body += str(messages) + "<br>"
##body += str(codesPast)
##body += str(list(codesCurrent[0]))
##body += str(selectAnalyses(cadiInfoCurrent, list(codesCurrent[0])))
#body += str(wgFilters) + "<br>"
#body += str(cadiInfoCurrent) + "<br>"
#body += str(cadiInfoPast) + "<br>"
#body += str(analysisFilters) + "<br>"
for analysisCode in codesCurrent:
  analysisDiff = htmlDiffInfo(selectAnalyses(cadiInfoPast, [analysisCode]), selectAnalyses(cadiInfoCurrent, [analysisCode]))
  if not (analysisDiff  == ""):
    body += "<h3>" + analysisCode + "</h3><br>"
    body += analysisDiff
  #body += htmlShowInfo(selectAnalyses(cadiInfoPast, [analysisCode]))
  #body += htmlShowInfo(selectAnalyses(cadiInfoCurrent, [analysisCode]))
servePage(body)
