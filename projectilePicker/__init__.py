from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

from rocketPicker import backend
from rocketPicker import simulate


@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/sim')
def sim():
    return render_template("simulate.html")

@app.route('/api')
def docs():
    return render_template("api.html")

@app.route('/api/main')
def main():
    return jsonify(backend.main())

@app.route("/api/search")
def search():
    name = request.args.get("name")
    return jsonify(backend.getRocketFromName(name).jsonify())

@app.route('/api/searchMotor')
def searchMotor():
    query = request.args.get("query")
    return jsonify(simulate.searchMotors(query))

@app.route('/api/create', methods=["POST"])
def create():
    try:
        name = request.form['name']
        manu = request.form['manu']
        diam = float(request.form['diam'])
        level = request.form['level']
        motor = float(request.form['motor'])
        img = request.form["img"]
        url = request.form["url"]
        price = request.form["price"]
        material = request.form["material"]
        mass = request.form["mass"]
        backend.newRocket(name=name, manufacturer=manu, diam=diam, level=level, motorSize=motor, img=img, url=url, price=price, material=material, mass=mass)

    except:
        return render_template("created.html", message="Failed- Server Issue")

    return render_template("created.html", message="Success!")


@app.route("/api/simulate")
def simu():
    name = request.args.get("rocketName")
    motorData = {
        "motorName":request.args.get("motorName"),
        "motorManu":request.args.get("motorManu")
    }
    rep = backend.sim(name, motorData)

    return jsonify(rep)

if __name__ == '__main__':
    app.run()