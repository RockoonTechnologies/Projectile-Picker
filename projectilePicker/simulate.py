import requests
import json
import numpy as np


class Motor:
    def __init__(self, man="", des="", name="", iclass="", diam=0):
        self.manufacturer = man
        self.designation = des
        self.commonName = name
        self.impulseClass = iclass
        self.diameter = diam

    def jsonify(self):
        return {
            "manufacturer": self.manufacturer,
            "designation": self.designation,
            "commonName": self.commonName,
            "impulseClass": self.impulseClass,
            "diameter": self.diameter,
            "availability": "available",
        }


def searchMotors(query):
    data = {
        "commonName": query,
        "availability": "available",
        "maxResults": 10
    }
    r = requests.post('https://www.thrustcurve.org/api/v1/search.json', data =json.dumps(data))
    print(r)
    reps = []
    for item in r.json()["results"]:
        reps.append(item)

    return reps


def sim(rocket, motor):

    p = 1.2
    cD = .6
    g = -9.8
    A = (0.25 * np.pi * (rocket.diameter * rocket.diameter)) / 1000
    print(A)
    tb = motor["burnTimeS"]
    F = motor["avgThrustN"]
    m = rocket.mass + motor["totalWeightG"]
    Em = m - motor["propWeightG"]

    k = .5 * p * cD * A

    burnoutAltitude = (m / k) * np.log(np.cosh((tb / m) * np.sqrt(k * (F - m * g))))
    burnoutVelocity = (np.sqrt((F-(m*g) / k)) * np.tanh((tb/m) * np.sqrt(k * (F - m*g))))
    coastAltitude = (Em / (2 * k)) * np.log(((k * np.power(burnoutVelocity, 2)) / Em * -g) + 1)
    coastTime = np.sqrt(Em/(-g*k)) * np.arctan(burnoutAltitude * np.sqrt(k/(-g * Em)))

    data = {
        "burnoutAltitude": burnoutAltitude,
        "burnoutVelocity": burnoutVelocity,
        "coastAltitude": coastAltitude,
        "coastTime": coastTime,
        "totalTime": tb + coastTime,
        "apogee": burnoutAltitude + coastAltitude
    }
    return data