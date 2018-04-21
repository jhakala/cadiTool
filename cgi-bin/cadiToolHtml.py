def getHeader():
  header = """
<html>
  <head>
     <title>cadiTool</title>
     <link href="https://fonts.googleapis.com/css?family=Open+Sans:400italic,600italic,700italic,400,600,700" rel="stylesheet" type="text/css">
     <link rel="stylesheet" type="text/css" href="cadiTool.css"> 
     <!-- <link rel="icon" type="image/png" href="cadiTool.icon"> -->
     <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
     <style>
       body {
          font-family: Consolas,monaco,monospace; 
       }
       table {
         font-size: 12px;
       }
       .diff td{
          padding-right: 8px;
        }
       .diff_add {
         background-color: #ddffdd;
       }
       .diff_chg {
         background-color: #ffffbb;
       }
       .diff_sub {
         background-color: #ffdddd;
       }
     </style>
  </head>
  <body>
    <div id="top"><!--<img src="cadiToolLogo.png" width="50px">--><h1>cadiTool alpha</h1></div>
    <div id="wrapper">
    <!-- end header -->
""" 
  return header

def getFooter():
  footer =  """
    <!-- begin footer -->
    </div>
  </body>
</html>
"""
  return footer

def servePage(body):
  print "Content-type: text/html"
  print
  print getHeader()
  print body
  print getFooter()
