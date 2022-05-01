# export FLASK_APP=processor.py
# export FLASK_DEBUG=1 
# flask run

# imports
from flask import Flask, request, render_template
import json
from Indexer import indexerScript

# function which reads pickle file list from disk and merges to single inv idx
def unPickle():
  import pickle
  pickle_in = open('listPickle','rb')
  unpickledLists = pickle.load(pickle_in)
  invInd = {}
  for tup in unpickledLists:
    term = tup[0]
    if term in invInd:
      currList = invInd[term]
      if tup not in currList:
        currList.append(tup)
        invInd[term] = currList
    else: 
      invInd[term] = [(tup)]
  return invInd

invInd = unPickle()
#print(invInd["$penguin$"])

app = Flask(__name__)

@app.route("/query")
def queryVectorizer(query, tokenizedDocList):
  from indexerScript import queryVector
  return(queryVector(query,tokenizedDocList))

@app.route("/cosSim")
def cosSim(query, invInd):
  from indexerScript import cosineSimilarity, getTokenizedDocList 
  return(cosineSimilarity(queryVectorizer(query, getTokenizedDocList),invInd))

@app.route('/', methods=['GET','POST'])
def startQuery():
      query = request.form.get("query")
      jsonQuery = '{"Query": "' + str(query) + '"}'
      results = cosSim(query, invInd)
      print(results[:10])
      json_object = json.loads(jsonQuery)
    #  print(json_object)
      return render_template("home.html", jquery = json_object)

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)
