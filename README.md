# python-web-crawler

A web crawler built in Python, along with a console-based search engine.

# Installation
From Github
```
git clone https://github.com/sasindumaheepala/python-web-crawler
```
Move to directory
```
cd python-web-crawler
```


# Quickstart
When in directory:
Install requirements
```
pip install -r requirements.txt
```
Run program
> WARNING: DO NOT TRY RUNNING FILE DIRECTLY BY CLICKING THE FILE. Always use cmd or terminal. Otherwise permission errors may occur while trying to open database.csv. If this persists to happen through cmd of terminal, try opening these with administrator access.
```
python main.py
```

# Usage
### To use the web crawler:
When prompted with:
```
Choose what you want to do:
1 - Use web crawler
2 - Use web crawler and search engine
1 or 2
```
Select:
```
1
```

Follow instructions to use web crawler.

### To use search engine:
When prompted with:
```
Choose what you want to do:
1 - Use web crawler
2 - Use web crawler and search engine
1 or 2
```
Select:
```
2
```

Search engine will use the default database, which has crawled a few of the most popular websites on the internet such as google.com and wikipedia.org.

If the database requires to be updated a crawling process will begin, followed by the message:

```
Database Updated.
```

Otherwise, or after the update process an input asking for a search query will be shown.

```
Search Query:
```

To close the file just close the terminal or cmd window, or CTRL/CMD+C.
