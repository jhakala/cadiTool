#!/opt/rh/python27/root/usr/bin/python

import cgi
import cgitb; cgitb.enable() # for troubleshooting
from cadiInfoHistory import getCadiInfo
from cadiToolHtml import servePage

def getPhysWGs():
  cadiInfo = getCadiInfo()[1]
  output = set()
  for analysis in cadiInfo:
    output.add(analysis[u"physWG"])
  return output

def makeSubmitButton(form):
  html =       "      <form action='cadiToolDiffs.py'>"
  for key in form.keys():
    for filter in form.getlist(key):
      html +=  "        <input type='hidden' name={0} value={1}>".format(key, filter)
  html +=      "        hours in the past to check for changes in CADI: <input type='number' name='pastHours' value='24'>"
  html +=      "        <input type='submit' value='Show all differences'>"
  html +=      "      </form>"
  return html
  

def makeSplashPage(form):
  body =    makeSubmitButton(form)
  body +=      "      <br> OR: <br> "
  body +=      "      <h2>Select physics working group(s):</h2>\n"
  body +=      "        <form action='cadiToolHome.py'>\n"
  for physWG in getPhysWGs():
    body +=    "          <input type='checkbox' value='{0}' name='physWG'>{0}<br>\n".format(physWG)
  body +=      "        <input type='submit'>\n"
  body +=      "      </form>"
  return body
  

form = cgi.FieldStorage()
if not form.getvalue('physWG'):
  servePage(makeSplashPage(form))

else:
  servePage(makeSubmitButton(form))
  
