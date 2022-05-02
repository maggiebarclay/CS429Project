# export FLASK_APP=processor.py
# export FLASK_DEBUG=1 
# flask run


# imports
from unittest import result
from flask import Flask, request, render_template
import json
import string
import pickle
from indexerScript import cosineSimilarity, queryVector


# function which reads pickle file list from disk and merges to single inv idx
def unPickle():
  pickle_in = open('invIndPickle','rb')
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
  pickle_in = open('tokPickle','rb')
  tokenizedDocs = pickle.load(pickle_in)
  return (invInd, tokenizedDocs)

invInd = unPickle()[0]
tokenizedDocs = unPickle()[1]


app = Flask(__name__)


@app.route('/', methods=['POST'])
def startQuery():
  jquery = " "

  if request.method == 'POST':
    render_template('home.html',  jquery = "")
    query = request.form.get("query")
    jquery = {}
    jquery["Query"] = query
    results = cosineSimilarity(queryVector(tokenizedDocs, jquery["Query"]), invInd)
    return render_template("home.html", jquery = results[:10])

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)



