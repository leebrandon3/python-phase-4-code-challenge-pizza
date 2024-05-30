#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get('/restaurants')
def all_restaurants():
    return [restaurant.to_dict() for restaurant in Restaurant.query.all()], 200

@app.get('/pizzas')
def all_pizzas():
    return [pizza.to_dict(rules=["-restaurant_pizzas"]) for pizza in Pizza.query.all()]

@app.get('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if restaurant:
        return restaurant.to_dict(rules=["-restaurant_pizzas.restaurant"]), 200
    else:
        return {'error': 'Restaurant not found'}, 404

@app.delete('/restaurants/<int:id>')
def delete_restaurant(id):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Restaurant not found'}, 404

@app.post('/restaurant_pizzas')
def new_restaurant():
    try:
        restaurant_pizzas = RestaurantPizza(
            price = request.json['price'],
            pizza_id = request.json['pizza_id'],
            restaurant_id = request.json['restaurant_id']
        )
        db.session.add(restaurant_pizzas)
        db.session.commit()
        return restaurant_pizzas.to_dict(), 201
    except:
        return {"errors": ["validation errors"]}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
