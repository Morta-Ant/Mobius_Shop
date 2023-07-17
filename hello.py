from flask import Flask, render_template, jsonify
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
import json

app = Flask(__name__)
nav = Nav(app)

with open("database.json", "r") as d:
  data = json.load(d)

categories = sorted(set([item["category"] for item in data]))
categories_sub = Subgroup("Categories")

for cat in categories:
    categories_sub.items.append(View(cat, "category", cat = cat))

topbar = Navbar(
    "Top_bar",
    View("Home", "index"),
    View("All Products", "all_cats"),
    categories_sub,
    View("About Mobius", "about")
)

nav.register_element("top", topbar)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/<name>")
def product(name):
    item_data = get_item_from_data(name, data)
    return render_template("product.html", 
                           name = item_data["name"], 
                           price = item_data["price"], 
                           desc = item_data["desc"], 
                           img1 = item_data["images"][0],
                           img2 = item_data["images"][1])

@app.route("/category")
def all_cats():
    return render_template("show_all.html", data = data)

@app.route("/category/<cat>")
def category(cat):
    cat_items = items_by_cat(cat, data)
    return render_template("category.html", cat_items = cat_items)
    
@app.route("/about")
def about():
    return render_template("about.html")

def items_by_cat(cat, data):
    cat_items = []
    for item in data:
        if item["category"] == cat:
            cat_items.append(item)
    return cat_items

def get_item_from_data(name, data):
    for item in data:
        if item["name"] == name:
            return item

if __name__ == '__main__':
    nav.init_app(app)
    app.run(debug=True)