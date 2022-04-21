# CS429Project

The proposed system is comprised of three main components:
A Scrapy based Crawler
Will download web documents in html format
The seed will be initialized using a seed URL/Domain
A max number of pages / max depth will be set 
A scikit-learn based Indexer 
Will construct an inverted index in pickle format 
TF-IDF score / weight representation
Cosine similarity
Flask based Processor 
Will handle free text queries in json format
Query validation / error checking
Top-K ranked results