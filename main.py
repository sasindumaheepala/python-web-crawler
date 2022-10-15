from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv
import os
import difflib
import re

class Crawler:
	def __init__(self, database):
		# Creates CSV Database file if non-existent
		datafile = Path(database)
		if not datafile.is_file():
			with open(database, 'w', encoding="utf8") as file:
				file.write('id,url,title,description,response\n')
		self.path_to_database = database
		self.database = []
		with open(self.path_to_database, "r", encoding="utf8") as file:
			csv_reader = csv.DictReader(file)
			line_count = 0
			for row in csv_reader:
				next = {}
				for x,y in row.items():
					next[x] = y
				self.database.append(next)

	def crawl(self, websites, expand=False, exclude=[], autoinsert=True, maxnew=1, continuesearch=False, updatestatus=True):
		updatedwebsites = []
		if continuesearch and continuesearch <= len(self.database):
			for x in self.database:
				updatedwebsites.append(x["url"])
			websites = updatedwebsites
			current = len(updatedwebsites)-continuesearch
		else:
			current = 0
		original = len(self.database)
		max_original = maxnew
		numnew = 0
		while current < len(websites) and numnew < maxnew:
			URL = websites[current]
			page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
			soup = BeautifulSoup(page.content, "html.parser")
			try:
				title = soup.find_all("title")[-1].decode_contents().replace("\n", "<br>")
			except:
				title = ""
			try:
				description = soup.find_all("meta", {'name':'description'})[-1].get("content").replace("\n", "<br>")
			except:
				description = ""
			if title == "" and description == "":
				current += 1
				continue
			exists = False
			for x in self.database:
				if x["url"] == URL:
					exists = int(x["id"])
			if autoinsert and page.status_code not in exclude:
				if exists:
					updated = []
					with open(self.path_to_database, "r", encoding="utf8") as file:
						reader = csv.reader(file)
						updated = list(reader)
					updated[exists] = [exists, URL, title, description, page.status_code]
					with open(self.path_to_database, 'w', encoding="utf8") as file:
						writer = csv.writer(file)
						writer.writerows(updated)
					maxnew += 1
						
				else:
					with open(self.path_to_database, "a", encoding="utf8") as file:
						fieldnames = ['id', 'url', 'title', 'description', 'response']
						csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
						if exists:
							next_row = {'id': len(self.database), 'url': URL, 'title': title, 'description': description, 'response': page.status_code}
						else:
							next_row = {'id': (len(self.database)+1), 'url': URL, 'title': title, 'description': description, 'response': page.status_code}
						csv_writer.writerow(next_row)
						self.database.append(next_row)
			else:
				maxnew += 1
			if expand:
				links =  soup.find_all("a")
				new = []
				for link in links:
					next = link.get("href")
					try:
						if next.startswith("/"):
							next = next[1:]
						if not next.startswith("http"):
							if not URL.endswith("/"):
								URL += "/"
							next = URL+next
						if next.endswith("/"):
							next = next.rstrip("/")
						new.append(next)
					except:
						print()
				websites.extend(new)
				websites = list(dict.fromkeys(websites))
			current += 1
			numnew += 1
		
			# Updates console with info about crawler status
			if updatestatus:
				os.system("clear")
				print(f"Crawled: {current}. Inserted: {(len(self.database)-original)}/{max_original}. Total in database: {len(self.database)}.")

	def display_data(self):
		with open(self.path_to_database, "r", encoding="utf8") as file:
			csv_reader = csv.DictReader(file)
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					print(f'Column names are {", ".join(row)}\n')
					line_count += 1
				for x,y in row.items():
					print(f"{x} : {y}")
				print()
				line_count += 1
			print(f'Processed {(line_count-1)} row(s) of data.')


class Search(Crawler):
	def __init__(self, database, websites, minvals):
		Crawler.__init__(self, database)
		if len(self.database) < minvals:
			self.crawl(websites, expand=True, exclude=[404], maxnew=minvals-len(self.database), continuesearch=len(database), updatestatus=True)
			os.system("clear")
			print("Database Updated.")

	def search(self, query):
		results = []
		output = {}
		for item in self.database:
			val_1 = difflib.SequenceMatcher(None,item["title"].lower().split(),query.lower().split()).ratio()
			val_2 = difflib.SequenceMatcher(None,item["description"].lower().split(),query.lower().split()).ratio()
			average = (val_1 + val_2)/2
			results.append([item["id"], average, 2])

		for result in results:
			if result[1] in output:
				output[result[1]].append(result[0])
			else:
				output[result[1]] = [result[0]]

		return dict(reversed(dict(sorted(output.items())).items()))
		

# following function adapted from an answer on https://stackoverflow.com/questions/21659044/how-can-i-prepend-http-to-a-url-if-it-doesnt-begin-with-http
def format_URL(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

database = "database.csv"
websites = ["https://google.com", "https://youtube.com", "https://facebook.com", "https://twitter.com", "https://instagram.com", "https://baidu.com", "https://wikipedia.org", "https://yandex.ru", "https://yahoo.com", "https://whatsapp.com"]

os.system("clear")
print("Choose what you want to do:\n1 - Use web crawler\n2 - Use web crawler and search engine\n1 or 2")
action = input()

while action == "1":
	try:
		os.system("clear")
		print("Input what websites you want to start the crawler with. Input as many as you want, click enter with a blank line if you are done.")
		websites = []
		while True:
			next = input()
			if next.strip() != "":
				websites.append(format_URL(next))
				continue
			break
			
		database = input("Choose what to call you database. This will be stored as a csv file: {your database name}.csv.\n") + ".csv"
		spider = Crawler(database)
		spider.crawl(websites, expand=True, exclude=[404], maxnew=int(input("How many webpages would you like to crawl? ")))
		if input("Would you like you display crawler database? (Y/n) ").lower() == "y":
			spider.display_data()
		break
	except Exception as e:
		print(e)

while action == "2":
	try:
		search = Search(database, websites, 500)
		query = input("\033[1mSearch Query: ")
		print("\n\033[0m")
		output = search.search(query)
		total = 0
		for x, y in output.items():
			if x == 0.0:
				break
			for out in y:
				if total == 9:
					break
				result = search.database[(int(out)-1)]
				print(f"""\033[94m{result["url"]}\033[0m\033[95m\n{result["title"].strip()}\033[0m\n{result["description"].strip()}\n""")
				total += 1
		if len(output) == 1:
			print("\033[93mNo results found.\033[0m\n")
	except Exception as e:
		print(e)
		continue
