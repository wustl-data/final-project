import bs4
from bs4 import BeautifulSoup
import requests
import re
import csv

url = "https://www.pro-football-reference.com/players/W/WilsRu00.htm"

data = requests.get(url)
html = BeautifulSoup(data.text, 'html.parser')

content = str(html.find("tr", {"class":"full_table"}))
size = len("\"<tr class=\"full_table\" id=\"passing.\"")
year = content[size:]
print(content)

