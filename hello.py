from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/<name>")
def product(name):
    item_data = get_item_from_data(name, data)
    return render_template("product.html", 
                           **item_data
                           )

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

def import_data():
    with open("database.json", "r") as d:
        data = json.load(d)
    return data

def get_categories(data):
    categories = sorted(set([item["category"] for item in data]))
    return categories

def setup_nav(categories):    
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

    nav = Nav()
    nav.register_element("top", topbar)
    nav.init_app(app)
    

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

    data = import_data()
    categories = get_categories(data)
    setup_nav(categories)

    app.run(debug=True)