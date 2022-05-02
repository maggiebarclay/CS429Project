
# get all of the info from html files
# two lists, one of the names one with the descriptions
  
if __name__ == "__main__":
# imports 
  import os
  import numpy as np
  from bs4 import BeautifulSoup
  import string
  import pickle
  import nltk
  nltk.download('punkt')
  from nltk.tokenize import word_tokenize

  characterList = []
  descriptionsList = []
  picturesList = []


  for filename in os.listdir("project_crawler/project_crawler/htmlFiles/"):   
      try:
          #print("reading file: " + str(filename))
          with open("project_crawler/project_crawler/htmlFiles/" + str(filename), 'r') as f:
              soup = BeautifulSoup(f, 'html.parser')
              character = soup.title.getText().split()[0]
              characterList.append(character)

              # appending separate, not sure if getting all description parts yet or just the first
              descList = []
              descList.append(soup.find_all('p')[1].getText().replace('\n',' '))
              descList.append(soup.find_all('p')[2].getText().replace('\n',' '))
              descList.append(soup.find_all('p')[3].getText().replace('\n',' '))

              description = "".join(descList)
              descriptionsList.append(description)

              image = soup.find('meta', property="og:image").get('content')
              picturesList.append(image)
              
      except:
          print(filename)
          print("This is being skipped,likely because of an unrecognized letter/character")
          pass

  notInvertedIndex = {}
  for i in range(len(characterList)):
    notInvertedIndex[characterList[i]] = (descriptionsList[i], picturesList[i])

  print("\npickling the 'not inverted index'")
  indexPickle = open('indexPickle','wb')
  pickle.dump(notInvertedIndex,indexPickle)
  indexPickle.close()

  tokenizedDocList = []

  def tokenizerMethod(docString: str):
    noPunctString = (docString.lower()).translate(str.maketrans('', '', string.punctuation))
    tokenizedDoc = word_tokenize(noPunctString)
    return tokenizedDoc

  for item in descriptionsList:
    tokenizedDocList.append(tokenizerMethod(item))

  print("\npickling tokenized doc list")
  tokPickle = open('tokPickle','wb')
  pickle.dump(tokenizedDocList,tokPickle)
  tokPickle.close()

  # TFIDF

  def calculateDF(tokenizedDocList: list):
    invInd = {}
    index = -1
    for doc in tokenizedDocList:
      index += 1
      for word in list(set(doc)):
        word = (word.lower()).translate(str.maketrans('', '', string.punctuation))
        word = "$" + word + "$"
        if word in invInd:
          currentDF = invInd[word]
          currentDF += 1
          invInd[word] = currentDF
        else: 
          invInd[word] = 1
    return invInd

  print("\npickling DF inv indx")
  calculateDF = calculateDF(tokenizedDocList)
  dfPickle = open('dfPickle','wb')
  pickle.dump(calculateDF,dfPickle)
  dfPickle.close()


  def makeInvInd(tokenizedDocList: list):
    invInd = {}
    index = -1
    #N is the number of docs 
    N = len(tokenizedDocList)

    pickle_in = open('dfPickle','rb')
    dfIndx = pickle.load(pickle_in)

    for doc in tokenizedDocList:
      index += 1
      for word in list(set(doc)):
        formatWord = '$' + word + '$'
        word = (word.lower()).translate(str.maketrans('', '', string.punctuation))
        #tf is how many times term appears in the document / len of doc <- going off of book so not dividing by length
        tf = doc.count(word)
        df = dfIndx[formatWord]
        idf = np.log(N/(df))
        tfidf = (tf*idf)

        if formatWord in invInd:    
          currList = invInd[formatWord]
          currList.append(((str(index),  str(characterList[index]), tfidf)))
          invInd[formatWord] = currList
          
        else:   
          invInd[formatWord] = [(str(index), str(characterList[index]), tfidf)]
    return invInd

  invIndex = makeInvInd(tokenizedDocList)

  numberOfBatches = 3

  def processDocs(tokenizedDocList, invIndex,numberOfBatches):
    start = 0

    blockSize = int(len(tokenizedDocList)/numberOfBatches)

    listOfTups = []

    for block in range(numberOfBatches):
      for i in range(start, start+blockSize):
        for term in tokenizedDocList[i]:
          term = "$" + term + "$"
          listOfTups.append((term, invIndex[term]))
      
      print("\nwriting block of docs with indecies: " + str(start) + " through " +  str(start+blockSize))
      invIndPickle = open('invIndPickle','wb')
      pickle.dump(listOfTups,invIndPickle)
      invIndPickle.close()

      start += blockSize

  processDocs(tokenizedDocList, invIndex, numberOfBatches)

def queryVector(docsList, query):
  import numpy as np
  import pickle
  print(query)
  query = query.split()
  queryIndx = {}
  pickle_in = open('dfPickle','rb')
  dfIndx = pickle.load(pickle_in)

  # idf = log (docs in corpus / docs with term in them)
  N = len(docsList)

  for term in query:
    term = "$" + term + "$"
    df = dfIndx[term]
    idf = np.log(N/(df))

    if term in queryIndx:    
        pass
    else:   
        queryIndx[term] = idf
  return queryIndx

def cosineSimilarity(query, index):
  import pickle
  scores = {}

  for query_term, query_weight in query.items():
      for charNum, character, doc_weight in index[query_term][0][1]:
        if character not in scores: 
          scores[character] = query_weight * doc_weight
        else:
          scores[character] += query_weight * doc_weight  
          
  finalScores = {}
  pickle_in = open('tokPickle','rb')
  tokenizedDocList = pickle.load(pickle_in)
  for character in scores.keys():
    finalScores[character] = (float(scores[character]) / (len(tokenizedDocList[int(charNum)])))

  return sorted(finalScores.items(), key=lambda x: x[1], reverse=True)

def getTokenizedDocList():
  return(tokenizedDocList)