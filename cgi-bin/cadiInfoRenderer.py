import json
from bs4 import BeautifulSoup

def deunicodeCadiInfo(cadiInfo):
  decoded = []
  for cadiLineDict in cadiInfo:
    nonunicode = dict([(str(k), str(v)) for k, v in cadiLineDict.items()])
    decoded.append(nonunicode)
  return decoded

def printInfo(cadiInfo):
  from pprint import pprint
  pprint(deunicodeCadiInfo(cadiInfo))

def htmlShowInfo(cadiInfo):
  import json2table
  html = "<ul>"
  for cadiLine in cadiInfo:
    html += "<li>" + json2table.convert(cadiLine)  + "</li>"
  html += "</ul>"
  return html

def htmlDiffInfo(cadiInfoOld, cadiInfoNew):
  import difflib
  htmlDiffer = difflib.HtmlDiff(wrapcolumn=90)
  oldInfoTableText = BeautifulSoup(htmlShowInfo(cadiInfoOld).replace("</tr>", "\n</tr><br>").replace("</th>",": </th>"))
  newInfoTableText = BeautifulSoup(htmlShowInfo(cadiInfoNew).replace("</tr>", "\n</tr><br>").replace("</th>",": </th>"))
  html = htmlDiffer.make_table(oldInfoTableText.get_text().splitlines(), newInfoTableText.get_text().splitlines(), "", "", True)
  if not "No Differences Found" in html:
    return html
  else:
    return ""

def selectAnalyses(cadiInfo, analyses):
  response = []
  for requestedAnalysis in analyses:
    response.append(
      (analysis for analysis in cadiInfo if str(analysis["code"]) == requestedAnalysis).next()
    )
  return response


def selectPhysWG(cadiInfo, physWGarr):
  codes = []
  for physWG in physWGarr:
    analyses = filter(lambda analysis: analysis['physWG'] == physWG, cadiInfo)
    for item in analyses:
      codes.append(item['code'])
  return (selectAnalyses(cadiInfo, codes), codes)
