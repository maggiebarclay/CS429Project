# export FLASK_APP=processor.py
# export FLASK_DEBUG = 1 
# flask run

# imports
import flask
from flask import Flask, request, render_template
import json
import html

app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def query():
     if request.method == "POST":
       query = request.form.get("query")
       return "Here are some relevant villagers for the query: "+ query
     return render_template("home.html")
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json'):
    #     json = request.json
    #     return json
    # else:
    #     return 'Content-Type not supported!'

if __name__=='__main__':
   app.run(use_reloader=True)
   app.run(host="0.0.0.0", port = 5000, debug=True)