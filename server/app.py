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

@app.get("/restaurants")
def get_restaurants():
    return [res.to_dict() for res in Restaurant.query.all()], 200

@app.get("/restaurants/<int:id>")
def get_by_id(id):
    res = Restaurant.query.where(Restaurant.id == id).first()
    if res:
        return res.to_dict(rules =("restaurant_pizzas",)), 200
    else:
        return { "error": 'Restaurant not found' }, 404

@app.delete("/restaurants/<int:id>")
def delete_res(id:int):
    res_to_delete = Restaurant.query.where(Restaurant.id ==id).first()
    if res_to_delete:
        db.session.delete(res_to_delete)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Restaurant not found'}, 404
    
    # feel this above is correct

@app.get('/pizzas')
def get_pizzas():
    return [pizza.to_dict() for pizza in Pizza.query.all()], 200

@app.post('/restaurant_pizzas')
def post_res_pizza():
    try:
        new_res_pizza = RestaurantPizza( 
            price = request.json.get("price"),
            pizza_id =request.json.get("pizza_id"),
            restaurant_id = request.json.get("restaurant_id"),
           
            
        )
        if new_res_pizza:
            db.session.add(new_res_pizza)
            db.session.commit()

            return new_res_pizza.to_dict(), 201
    
    except ValueError as error:
        return {'errors': ["validation errors"]}, 400
if __name__ == "__main__":
    app.run(port=5555, debug=True)
