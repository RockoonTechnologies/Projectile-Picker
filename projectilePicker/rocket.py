class Rocket:
    def __init__(self, name="N/A", manufacturer="N/A", diam=0, level="LPR", motorSize=18, img="static/imgs/placeholder.png", url="", price=0,material="", mass=0):
        self.name = name
        self.manufacturer = manufacturer
        self.diameter = diam

        self.level = level

        self.motorSize = motorSize

        self.img = img
        self.url = url

        self.price = price

        self.material = material
        self.mass = mass



    def jsonify(self):
        return {
            "name": self.name,
            "img": self.img,
            "manufacturer": self.manufacturer,
            "diameter": self.diameter,
            "level": self.level,
            "motor": self.motorSize,
            "url": self.url,
            "price": self.price,
            "material": self.material,
            "mass": self.mass
        }