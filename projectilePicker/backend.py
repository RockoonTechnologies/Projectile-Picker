import json
from rocketPicker.rocket import *
from rocketPicker import crawler
import threading
import time

from rocketPicker import simulate



instances = []

def save():
    data = main()
    with open('rocketPicker/save.json', 'w') as json_file:
        json.dump(data, json_file)


def load():
    with open('rocketPicker/save.json', 'r') as f:
        data = json.load(f)

    for item in data["data"]:
        new = Rocket(name=item["name"], manufacturer=item["manufacturer"], diam=item["diameter"], level=item["level"], motorSize=item["motor"], img=item["img"], url=item["url"], price=item["price"], material=item["material"], mass=item["mass"])
        safeAdd(new)


def main():
    data = {
        "data": [],
        "etc": None
    }
    for item in instances:
        data["data"].append(item.jsonify())


    data["etc"] = len(instances)
    return data

def safeAdd(rocket):
    global instances
    result = None
    for item in instances:
        if item.name == rocket.name:
            if item.diameter == rocket.diameter:
                result = item
                break

    if result == None:
        instances.append(rocket)
    else:
        instances.pop(instances.index(result))
        instances.append(rocket)
    save()


def newRocket(name="N/A", manufacturer="N/A", diam=0, level="LPR", motorSize=18, img="static/imgs/placeholder.png", url="", price=0, material="", mass=0):
    new = Rocket(name=name, manufacturer=manufacturer, diam=diam, level=level, motorSize=motorSize, img=img, url=url, price=price, material=material, mass=mass)
    safeAdd(new)

def getRocketFromName(name):
    for item in instances:
        if item.name == name:
            return item

def sim(rocketName, motor):
    rocket = getRocketFromName(rocketName)
    try:
        res = simulate.searchMotors(motor["motorName"])
        for item in res:
            if item["designation"] == motor["motorName"] and item["manufacturerAbbrev"] == motor["motorManu"]:
                motor = item
                break
    except:
        return {"Error": "Simulation Failed- failed to contact thrustcurve"}

    try:
        data = simulate.sim(rocket, motor)
        return data
    except:
        return {"Error": "Simulation Failed- Suspected reason: not enough sufficient motor information, this is most likely due to a bad entry on thrustcurve"}





def backgroundTask():
    load()
    totalList = []
    #apogee = crawler.apogee()
    print("Loaded Apogee")
    #totalList.extend(apogee)

    #rocketarium = crawler.rocketarium()
    #totalList.extend(rocketarium)
    print("loaded rocketarium")
    for item in totalList:
        safeAdd(item)

    print("done!")
    while True:
        time.sleep(500)
        save()


threading.Thread(target=backgroundTask).start()
