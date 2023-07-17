from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View

app = Flask(__name__)
nav = Nav(app)

nav.register_element("top", Navbar(
    "Top_bar",
    View("Home", "index"),
    View("Categories", "category"),
    View("About Mobius", "about")
))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/category")
def category():
    return render_template("categories.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    nav.init_app(app)
    app.run(debug=True)