
def get_keyword_id(input):
  keyword_id = connection.execute("SELECT keyword_id FROM keywords WHERE keyword=%s", % (input,))
  if (!keyword_id):
    connection.execute("INSERT INTO keywords VALUES(keyword) (%s);", % (input,))
    keyword_id = connection.execute("SELECT keyword_id FROM keywords WHERE keyword=%s", % (input,))
  return keyword_id


def get_fetch_date(keyword_id):
  date = connection.execute("SELECT fetchdate FROM keywords WHERE keyword_id=%d", % (keyword_id,))
  return fetchdate


def set_quizlet_json(parsed):
  for quizlet_id, json in parsed:
    connection.execute("INSERT INTO QuizletDecks VALUES(quizlet_id,json) (%s, %s);" %(quizlet_id,json)
    # suppose to have a certain list of quizlet_id's that we insert
    # and a bunch of jsons

def set_quizlet_keyword (keyword_id,parsed):
  for quizlet_id in parsed.iterkeys():
    connection.execute("INSERT INTO KeywordsQuizletDecks VALUES(keyword_id,quizlet_id) (%d,%d);",%(keyword_id,quizlet_id))

def getQuizletDecks(input):
  keyword_id=get_keyword_id(input)
  fetchdate=get_fetch_date(keyword_id)
  listOfQid=connection.execute("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
  if((!listOfQid) || fetchdate>7):
    parsed=get_parsed(??)
    set_quizlet_json(parsed)
    set_quizlet_keyword(keyword_id,parsed)
    listOfQid=connection.execute("SELECT quizlet_id FROM KeywordsQuizletDecks WHERE keyword_id=%d",%(keyword_id,))
    print("Done adding values")
  else:
    print("Pulling exisiting values...")
  return listOfQid
