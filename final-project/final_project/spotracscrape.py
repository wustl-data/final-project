import bs4
from bs4 import BeautifulSoup
import requests
import re
import csv

qbs = [("tampa-bay-buccaneers","tom-brady"), 
        ("green-bay-packers","aaron-rodgers"),
        ("los-angeles-chargers","justin-herbert"),
        ("cincinnati-bengals","joe-burrow"),
        ("kansas-city-chiefs","patrick-mahomes"),
        ("buffalo-bills","josh-allen"),
        ("arizona-cardinals","kyler-murray"),
        ("los-angeles-rams","matthew-stafford"),
        ("dallas-cowboys","dak-prescott"),
        ("las-vegas-raiders","derek-carr"),
        ("tennessee-titans","ryan-tannehill"),
        ("seattle-seahawks","russell-wilson"),
        ("minnesota-vikings","kirk-cousins"),
        ("baltimore-ravens","lamar-jackson"),
        ("philadelphia-eagles","jalen-hurts"),
        ("atlanta-falcons","matt-ryan"),
        ("new-england-patriots","mac-jones"),
        ("san-francisco-49ers","jimmy-garoppolo"),
        ("denver-broncos","teddy-bridgewater"),
        ("indianapolis-colts","carson-wentz"),
        ("new-orleans-saints","jameis-winston"),
        ("miami-dolphins","tua-tagovailoa"),
        ("detroit-lions","jared-goff"),
        ("cleveland-browns","deshaun-watson"),
        ("new-york-giants","daniel-jones"),
        ("pittsburgh-steelers","mitchell-trubisky"),
        ("washington-football-team","taylor-heinicke"),
        ("chicago-bears","justin-fields"),
        ("houston-texans","davis-mills"),
        ("jacksonville-jaguars","trevor-lawrence"),
        ("carolina-panthers","sam-darnold"),
        ("new-york-jets","zach-wilson")]

contract_data = []

for qb in qbs:
    team = qb[0]
    player = qb[1]
    print(player)
    url = 'https://www.spotrac.com/nfl/{}/{}/'.format(team, player)

    if(player == "russell-wilson"):
        years = "4"
        money = "$140,000,000"
    else:
        data = requests.get(url)
        html = BeautifulSoup(data.text, 'html.parser')

        content = str(html.find("span", {"class":"contract-type-years"}))

        if(content!="None"):
            content = content[content.index(">")+1:]
            previous_contract_years = content[:content.index("<")]
            print(previous_contract_years)

            content = html.find("p", {"class": "currentinfo"})
            content = str(content)
            contract_info = content[content.index(" a")+2:content.index("contract")]

            years = contract_info[:contract_info.index(",")].strip().split(" ")[0]
            money = contract_info[contract_info.index(",")+1:].strip()
            money = money.replace(",",'')
            money = money.replace("$",'')
            moneyPerYear = int(money)/int(years)

            content = str(html.find("span", {"class":"player-infoitem"}))
            age = content[content.index(">")+1:]
            age = age[:age.index("-")].strip()
        
            player = player.replace("-"," ").title()


            contract_data.append([player,years,money,moneyPerYear,age,previous_contract_years])

f = open('salaryData.csv', 'w')

writer = csv.writer(f)
writer.writerow(["QB Name","Number of Years on Contract", "Total Contract Size","Salary per Year","Age","Previous Contract Years"])

for contract in contract_data:
    writer.writerow(contract)

f.close()


