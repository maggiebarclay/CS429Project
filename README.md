# CS429Project

TO RUN THE APPLICATION: 

-> DOWNLOAD CODE LOCALLY
-> INSTALL NECESSARY PACKAGES (use the generated requirements.txt to install)
-> OPEN IN BROWSER http://127.0.0.1:5000/search
-> YOU SHOULD NOT NEED TO RERUN THE WEB CRAWLER
    -> IF DESIRED, RUN 'scrapy crawl webby' IN THE FIRST project_crawler DIRECTORY
-> YOU SHOULD NOT NEED TO RERUN THE INDEXER 
    -> ANY PARTS THAT ARE UTILIZED BY THE PROCESSOR IN REALTIME SEARCH ARE ACCESSED AUTOMATICALLY THROUGH THE PROCESSOR.PY CODE
    -> IF DESIRED, RUN 'python indexerScript.py' (CS429Project > app > indexerScript.py)
-> START FLASK APP BY RUNNING python processor.py (CS429Project > app > indexerScript.py)
    -> ALTERNATIVELY, export FLASK_APP=processor AND THEN python -m flask run
