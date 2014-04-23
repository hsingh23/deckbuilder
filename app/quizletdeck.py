
def getKeywordId(input):
keyword_id=mysql.query("SELECT keyword_id FROM keywords WHERE keyword=%s",%(input,))
if (!keyword_id):
  mysql.query("INSERT INTO keywords VALUES(keyword) (%s);",%(input,))
  keyword_id=mysql.query("SELECT keyword_id FROM keywords WHERE keyword=%s",%(input,))
return keyword_id

def getFetchDate(keyword_id):
date=mysql.query("SELECT fetchdate FROM keywords WHERE keyword_id=%d",%(keyword_id,))
return fetchdate

def getParsed(??):
#don't know how to get the parsed data, probably an http call

def setQuizletJson(parsed):
for quizlet_id, json in parsed:
  mysql.query("INSERT INTO QuizletDecks VALUES(quizlet_id,json) (%s, %s);" %(quizlet_id,json)
  #suppose to have a certain list of quizlet_id's that we insert
  #and a bunch of jsons

def setQuizletKeyword(keyword_id,parsed):
for quizlet_id in parsed.iterkeys():
  mysql.query("INSERT INTO KeywordsQuizletDecks VALUES(keyword_id,quizlet_id) (%d,%d);",%(keyword_id,quizlet_id))

def getQuizletDecks(input):
keyword_id=getKeywordId(input)
fetchdate=getFetchDate(keyword_id)
listOfQid=mysql.query("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
if((!listOfQid) || fetchdate>7):
  parsed=getParsed(??)
  setQuizletJson(parsed)
  setQuizletKeyword(keyword_id,parsed)
  listOfQid=mysql.query("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
  print("Done adding values")
else:
  print("Pulling exisiting values...")
return listOfQid


Trigger stuff - in QuizletDecks
if(!quizlet_id)
  Insert JSON into QuizletDecks
else:
  Update JSON in QuizletDecks
