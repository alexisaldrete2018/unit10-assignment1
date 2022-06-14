
from crypt import methods
from math import prod
from flask import Flask, request
from flask import abort
from about_me import me
from mock_data import catalog
import json
from config import db
from bson import ObjectId

app = Flask('assignment2')

@app.route("/", methods=["GET"])
def home():
    return "This is the home page"

@app.route("/about")
def about():
    return (me["first"] +" "+ me["last"])

@app.route("/myaddress")
def address():
    return (me["address"]["street"] + " " + me["address"]["number"])


    ################## ENDPOINTS ##################

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({})

    for product in cursor:
        results.append(product)

    return json.dumps(results)

@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)

@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    count = 0
    cursor = db.products.find({})

    for product in cursor:
        count+=1

    return json.dumps(count)

@app.route("/api/catalog/<id>", methods=["GET"])
def get_product(id):
    for prod in catalog:
        if prod["_id"]==id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")

@app.route("/api/catalog/total", methods=["GET"])
def get_total():
    total = 0
    cursor = db.products.find({})

    for product in cursor:
        price = product["price"]
        total += price

    return json.dumps(total)

@app.route("/api/products/<category>", methods=["GET"])
def get_category(category):
    products = []
    for product in catalog:
        if product["category"]==category.lower():
            products.append(product)
    return json.dumps(products)

@app.route("/api/categories", methods=["GET"])
def get_categories():
    categories = []
    for product in catalog:
        category = product["category"]
        if category not in categories:
            categories.append(category)
    return json.dumps(categories)

@app.route("/api/catalog/cheapest", methods=["GET"])
def get_cheapest():
    minPrice = ""
    cursor = db.products.find({})
    for product in cursor:
        if(minPrice == ""):
            minPrice = product["price"]
        else:
            if(product["price"]<minPrice):
                minPrice = product["price"]
    return json.dumps(minPrice)
    
app.run(debug=True)