# Projectile Picker
a db of filterable, searchable, and editable Rocket kits.

## Shortcuts

See it Running Here: https://rocketpicker.herokuapp.com/

It also provides a public REST API you can find here: https://rocketpicker.herokuapp.com/api


### The Code

**Brief Warning: this code hasnt been "cleaned"**

`__init__.py` hosts the webpage, API, and everything else via Flask (at deployment, it uses Gunicorn as well)- it also connects to the backend

`backend.py` runs the "db" and further distrobutes stuff to the following files:

`rocket.py` holds the `Rocket` class which acts as a data struct for literally everything

`crawler.py` is a simple code that searches rocket websites for kits, then tries to add them to the db. So far it only does Apogee and Rocketarium because it was easy :p

`simulate.py` is a basic, crappy simulation thingy. It also acts as a shell for thrustcurve.org 

## Roadmap

1. Connect Domain (if heroku wouldnt stop being a turd nugget)
2. Switch to Mongodb
3. fix simulations
4. actually make it look "good"

