from urllib.request import urlopen
import urllib.error
import json
import sqlite3
import ssl

url = 'http://api.plos.org/search?q=title:DNA'

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Docs')
cur.execute('''
            CREATE TABLE IF NOT EXISTS Docs
            (id TEXT, journal TEXT, eissn TEXT, publication_date TEXT, 
            article_type TEXT, abstract TEXT, title_display TEXT, score REAL)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

try:
    js = json.loads(data)
except:
    js = None

for item in js["response"]["docs"]:
    cur.execute('''INSERT INTO Docs (id, journal, eissn, publication_date, article_type, abstract, title_display, score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    , (item["id"], item["journal"], item["eissn"], item["publication_date"], item["article_type"],
    item["abstract"][0], item["title_display"], item["score"]))

    #print(item["id"],'\n', item["journal"], '\n', item["eissn"], '\n', item["publication_date"], '\n', item["article_type"],
    #'\n', item["abstract"][0], '\n', item["title_display"], '\n', item["score"])
    conn.commit()

cur.close()