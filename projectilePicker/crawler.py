import pandas as pd
import requests
import time
from rocketPicker import rocket
from bs4 import BeautifulSoup
import random
pd.options.display.max_columns = None

def getLevelFromPad(input):
    if input == "High Power":
        return "HPR"
    if input == "Mid Power":
        return "MPR"
    else:
        return "LPR"


def getURLfromText(array, text):
    for item in array:
        if text == item.string:
            return item["href"]

def apogeeImg(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    div = soup.find(id="productMainImage")

    a = div.findChildren("a")[0].findChildren("img")[0]["src"]
    return "https://www.apogeerockets.com/" + a

def apogee():
    content = requests.get("https://www.apogeerockets.com/index.php?main_page=sortable_rockets_list&m=catalog").content
    df = pd.concat(pd.read_html(content))
    soup = BeautifulSoup(content, "lxml")
    urls = soup.find_all("a")
    total = []

    for index, row in df.iterrows():

        name = row["Rocket Name"]
        if "pack" in name:
            continue

        manu = row["Manuf."]
        dia = None
        if "Varies" in row["Diameter"]:
            continue
        if "Max" not in row["Diameter"]:
            dia = round(float(row["Diameter"].split('"')[0]) * 25.4, 2)
        else:
            dia = round(float(row["Diameter"].replace("Max:", "").split('"')[0]) * 25.4, 2)

        motor = float(row["Motor Size"].replace("mm", ""))
        level = getLevelFromPad(row["Launch Pad"])
        price = float(row["Price"].replace("$", ""))
        mass = 0
        if "kg" in row["Weight"]:
            mass = float(row["Weight"].split("(")[1].replace("kg)", "")) * 1000
        else:
            mass = float(row["Weight"].split("(")[1].replace("g)", ""))

        url = getURLfromText(urls, name)
        img = apogeeImg(url)

        new = rocket.Rocket(name=name, manufacturer=manu, diam=dia, motorSize=motor, level=level, price=price, mass=mass, url=url, img=img)
        total.append(new)

        print(index)



    return total


def rocketariumMini(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, "lxml")
    name = soup.find("h3", id="productName").getText()
    price = float(soup.find("h3", id="productPrices").getText().strip().replace("$", " "))
    img = soup.find_all("img")
    img = random.choice(img)["src"]

    diam = 0
    mass = 0
    for item in soup.find_all("p"):
        if "Length" in item.getText():
            splitted = item.getText().split("\n")
            for str in splitted:
                if str == "\r":
                    splitted.pop(splitted.index(str))
                else:
                    str = str.strip()
            diam = float(splitted[1].split("(")[1].replace("mm)", ""))
            mass = float(splitted[2].split("(")[1].replace("g)", ""))

    return rocket.Rocket(name=name, price=price, img=img, diam=diam, mass=mass, url=url, manufacturer="Rocketarium")


def rocketarium():
    content = requests.get("https://www.rocketarium.com/Rockets").content
    soup = BeautifulSoup(content, "lxml")

    a = soup.find_all("a")
    goodList = []
    for item in a:
        if item["href"].startswith("https://www.rocketarium.com/Rockets/"):
            goodList.append(item)

    finalList = []
    for item in goodList:
        try:
            finalList.append(rocketariumMini(item["href"]))
        except:
            pass
    return finalList



