# export FLASK_APP=processor.py
# export FLASK_DEBUG = 1 
# flask run

# imports
import flask
from flask import Flask, request, render_template
import json
import pickle

# function which reads pickle file list from disk and merges to single inv idx
def unPickle():
  pickle_in = open('listPickle','rb')
  unpickedLists = pickle.load(pickle_in)
  invInd = {}
  for tup in unpickedLists:
      if tup[0] in invInd:
        currList = invInd[tup[0]]
        currList.append(str(tup[1]))
        invInd[tup[0]] = currList
      else: 
        invInd[tup[0]] = [str(tup[1])]
  for x, y in invInd.items():
    invInd[x] = (list(set(y)))
  return invInd
invInd = unPickle()
print(invInd)



app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def query():
     if request.method == "POST":
       query = request.form.get("query")
       jsonQuery = '{"Query": "' + query + '"}'
       json_object = json.loads(jsonQuery)
       #print(json_object)
       return render_template("home.html", jquery = json_object)
    

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)
