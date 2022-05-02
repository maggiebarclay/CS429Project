# export FLASK_APP=processor.py
# export FLASK_DEBUG=1 
# flask run


# imports
from unicodedata import name
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
  pickle_in = open('indexPickle','rb')
  notInvInd = pickle.load(pickle_in)
  return (invInd, tokenizedDocs, notInvInd)

invInd = unPickle()[0]
tokenizedDocs = unPickle()[1]
notInvInd = unPickle()[2]

app = Flask(__name__)

@app.route('/search')
def form():
    return render_template('form.html')
 
@app.route('/results', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"Please add '/search' to the end of your url :-)"
    if request.method == 'POST':
        query = request.form.get("query")
        jquery = {}
        jquery["Query"] = query
        results = cosineSimilarity(queryVector(tokenizedDocs, jquery["Query"]), invInd)
        names = []
        for result in results[:10]:
          names.append(result[0])
        descriptions = []
        for name in names:
            descriptions.append(notInvInd[name])
        return render_template("data.html", query = query, results = zip(names, descriptions))

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)



