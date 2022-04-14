import bs4
from bs4 import BeautifulSoup
import requests
import re
import csv

from bs4 import BeautifulSoup
import requests

url = "https://www.pro-football-reference.com/players/W/WilsRu00.htm"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Get table
table = soup.find(class_="table_outer_container")

# Get head
thead = table.find('thead')
th_head = thead.find_all('th')

for thh in th_head:
    # Get case value
    print(thh.get_text())

    # Get data-stat value
    print(thh.get('data-stat'))

# Get body
tbody = table.find('tbody')
tr_body = tbody.find_all('tr')

for trb in tr_body:
    # Get id
    print(trb.get('id'))

    # Get th data
    th = trb.find('th')
    print(th.get_text())
    print(th.get('data-stat'))

    for td in trb.find_all('td'):
        # Get case value
        print(td.get_text())
        # Get data-stat value
        print(td.get('data-stat'))

# Get footer
tfoot = table.find('tfoot')
thf = tfoot.find('th')

# Get case value
print(thf.get_text())
# Get data-stat value
print(thf.get('data-stat'))

for tdf in tfoot.find_all('td'):
    # Get case value
    print(tdf.get_text())
    # Get data-stat value
    print(tdf.get('data-stat'))

"""

url = "https://www.pro-football-reference.com/players/W/WilsRu00.htm"

data = requests.get(url)
html = BeautifulSoup(data.text, 'html.parser')

#content = str(html.find("tr", {"class":"full_table"}))
#size = len("\"<tr class=\"full_table\" id=\"passing.\"")
#year = content[size:]
#year = content[:10]


id = "passing.2018"
content = html.find("tr", {"id": id})
pass_cmp = html.find("data-stat")
pass_att = content.find("data-stat",{"id": "pass_att"})
pass_cmp_perc = content.find("data-stat",{"id": "pass_cmp_perc"})
pass_yds = content.find("data-stat",{"id": "pass_yds"})
pass_td = content.find("data-stat",{"id": "pass_td"})
pass_td_perc = content.find("data-stat",{"id": "pass_td_perc"})
pass_int = content.find("data-stat",{"id": "pass_int"})
pass_int_perc = content.find("data-stat",{"id": "pass_int_perc"})
pass_yds_per_att = content.find("data-stat",{"id": "pass_yds_per_att"})
pass_rating = content.find("data-stat",{"id": "pass_rating"})
pass_first_down = content.find("data-stat",{"id": "pass_first_down"})
comebacks = content.find("data-stat",{"id": "comebacks"})
pass_first_down = content.find("data-stat",{"id": "pass_first_down"})
awards = content.find("data-stat",{"id": "awards"})
print(pass_cmp)
print(pass_att)
print(pass_cmp_perc)
print(pass_yds)
print(pass_td)
print(pass_td_perc)
print(pass_int)
print(pass_int_perc)
print(pass_yds_per_att)
print(pass_rating)
print(pass_first_down)
print(comebacks)
print(pass_first_down)
print(awards)


# stats needed - cmp, att, cmp%, yds, td, int, int%, 1D, rate, y/a, gwd, awards

"""