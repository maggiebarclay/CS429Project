
# imports
from unicodedata import name
from unittest import result
from flask import Flask, request, render_template
import json
import string
import pickle
import nltk
nltk.download('punkt')
from indexerScript import cosineSimilarity, queryVector


# function which reads pickle file list from disk and merges to single inv idx
def unPickle():
  pickle_in = open('../invIndPickle','rb')
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
  pickle_in = open('../tokPickle','rb')
  tokenizedDocs = pickle.load(pickle_in)
  pickle_in = open('../indexPickle','rb')
  notInvInd = pickle.load(pickle_in)
  return (invInd, tokenizedDocs, notInvInd)

invInd = unPickle()[0]
tokenizedDocs = unPickle()[1]
notInvInd = unPickle()[2]


#########


# spell correct
def makeBigram(term):
    bigrams = [] 
    for i in range(len(term)-1):
      bigrams.append(term[i:i+2])
    return bigrams

def makeKGramInx(docsList):
  kGramIndx = {}
  for term in invInd.keys():
    bigramlist = makeBigram(term)
    for bigram in bigramlist:
      if bigram in kGramIndx:
        currList = kGramIndx[bigram]
        # no duplicates
        if term not in currList:
          currList.append(str(term))
          kGramIndx[bigram] = currList
      else: 
        kGramIndx[bigram] = [str(term)] 
  return kGramIndx

kGramIndx = makeKGramInx(tokenizedDocs)

def modifiedSearch(query):
  for term in query.split():
    term = "$" + term + "$"
    if term not in invInd:
      print("Error: your query has a term that does not match a term in the dictionary, here are some spelling correction options: \n")
      return(takeQuery2(term))

def takeQuery2(term):
  bigrams = makeBigram(term)
  print("The bigrams generated from query: \n" + str(bigrams) + "\n")
  bigramWordMatchList = []
  for bigram in bigrams:
    if bigram in kGramIndx:
      bigramWordMatchList.append(kGramIndx[bigram])

  print("All of words from kgram indx are (at least one bigram match): ")
  # flatten the list to remove dups
  bigramWordMatches = [item for sublist in bigramWordMatchList for item in sublist]
  bigramWordMatches = list(set(bigramWordMatches))
  print(bigramWordMatches)
  scoresList = []
  for word in bigramWordMatches:
    bigramScore = 0
    for bigram in bigrams:
      if bigram in word:
        bigramScore+=1
    scoresList.append(bigramScore)
  print("\n Scores list (how many sought after bigrams are in each of the above words?): ")
  print(scoresList)
  print("\n The words with the highest bigram score are: ")
  maxindx = []
  closeWords = []
  maxindx = [i for i, x in enumerate(scoresList) if x == max(scoresList)] 
  for i in maxindx:
    closeWords.append(bigramWordMatches[i])
  print(closeWords)
  editDistance = []
  #take out $ for edit dist
  term = term[1:-1]
  closeWords = [word[1:-1] for word in closeWords]
  for word in closeWords:
    editDistance.append(nltk.edit_distance(term, word))
  print("\n These are the edit distances: ")
  print(editDistance)
  print("\n Of the words, here are the ones with the smallest edit distance: ")
  correctionsList = []
  minInd = [i for i, x in enumerate(editDistance) if x == min(editDistance)] 
  for i in minInd:
    correctionsList.append(closeWords[i]) 
  print(correctionsList)
  return(correctionsList)

#########
app = Flask(__name__)

@app.route('/search',  methods = ['GET', 'POST'])
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
        corrections = {}
        results = []
        try: 
          results = cosineSimilarity(queryVector(tokenizedDocs, jquery["Query"]), invInd)
        except: 
          for term in query.split():
            if "$" + term + '$' not in invInd:
              if term in corrections:
                currList = corrections[term]
                currList.append((modifiedSearch(term)))
              else:
                corrections[term] = [(modifiedSearch(term))]
        names = []
        descriptions = []
        pictures = []
        for result in results[:10]:
          names.append(result[0])
        for name in names:
            descriptions.append(notInvInd[name][0])
            pictures.append(notInvInd[name][1])
        return render_template("data.html", query = query, results = zip(names, descriptions, pictures), corrections = corrections)

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)

