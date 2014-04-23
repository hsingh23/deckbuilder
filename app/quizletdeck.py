
def get_keyword_id(input):
  keyword_id = mysql.query("SELECT keyword_id FROM keywords WHERE keyword=%s", % (input,))
  if (!keyword_id):
    mysql.query("INSERT INTO keywords VALUES(keyword) (%s);", % (input,))
    keyword_id = mysql.query("SELECT keyword_id FROM keywords WHERE keyword=%s", % (input,))
  return keyword_id


def get_fetch_date(keyword_id):
  date = mysql.query("SELECT fetchdate FROM keywords WHERE keyword_id=%d", % (keyword_id,))
  return fetchdate


def get_parsed(??):
  # don't know how to get the parsed data, probably an http call
  pass


def set_quizlet_json(parsed):
  for quizlet_id, json in parsed:
    mysql.query("INSERT INTO QuizletDecks VALUES(quizlet_id,json) (%s, %s);" %(quizlet_id,json)
    # suppose to have a certain list of quizlet_id's that we insert
    # and a bunch of jsons

def set_quizlet_keyword (keyword_id,parsed):
  for quizlet_id in parsed.iterkeys():
    mysql.query("INSERT INTO KeywordsQuizletDecks VALUES(keyword_id,quizlet_id) (%d,%d);",%(keyword_id,quizlet_id))

def getQuizletDecks(input):
  keyword_id=get_keyword_id(input)
  fetchdate=get_fetch_date(keyword_id)
  listOfQid=mysql.query("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
  if((!listOfQid) || fetchdate>7):
    parsed=get_parsed(??)
    set_quizlet_json(parsed)
    set_quizlet_keyword(keyword_id,parsed)
    listOfQid=mysql.query("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
    print("Done adding values")
  else:
    print("Pulling exisiting values...")
  return listOfQid


# Trigger stuff - in QuizletDecks
# if(!quizlet_id)
#   Insert JSON into QuizletDecks
# else:
#   Update JSON in QuizletDecks
