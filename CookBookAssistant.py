from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

# JSON file path
DATA_FILE = "recipes.json"

# Load recipes
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save recipes
def save_data(recipes):
    with open(DATA_FILE, "w") as f:
        json.dump(recipes, f, indent=4)

# HTML template (inline for mobile)
template = """
<!DOCTYPE html>
<html>
<head>
<title>CookBook</title>
<style>
body { font-family: Arial; margin: 20px; background: #f8f8f8; }
h1 { color: #333; }
.card { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; }
input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
button { background: green; color: white; padding: 10px; border: none; cursor: pointer; }
a { text-decoration: none; color: blue; }
</style>
</head>
<body>
<h1>CookBook: Virtual Kitchen Assistant</h1>

<form method="GET" action="/">
<input type="text" name="search" placeholder="Search recipe..." value="{{ request.args.get('search','') }}">
<button type="submit">Search</button>
</form>

<a href="{{ url_for('add_recipe') }}">➕ Add New Recipe</a>

{% for recipe in recipes %}
<div class="card">
    <h2>{{ recipe.name }}</h2>
    <p><b>Time:</b> {{ recipe.time }}</p>
    <p><b>Ingredients:</b></p>
    <ul>
    {% for ing, qty in recipe.ingredients.items() %}
        <li>{{ ing }}: {{ qty }}</li>
    {% endfor %}
    </ul>
    <p><b>Steps:</b></p>
    <ol>
    {% for step in recipe.steps %}
        <li>{{ step }}</li>
    {% endfor %}
    </ol>
</div>
{% endfor %}
</body>
</html>
"""

# Add recipe template
add_template = """
<h1>Add New Recipe</h1>
<form method="POST">
    <input type="text" name="name" placeholder="Recipe Name" required>
    <textarea name="ingredients" placeholder="Ingredients (format: name=qty, one per line)" required></textarea>
    <textarea name="steps" placeholder="Steps (one per line)" required></textarea>
    <input type="text" name="time" placeholder="Cooking Time" required>
    <button type="submit">Save Recipe</button>
</form>
<a href="{{ url_for('home') }}">⬅ Back</a>
"""

@app.route("/", methods=["GET"])
def home():
    recipes = load_data()
    search_query = request.args.get("search", "")
    if search_query:
        recipes = [r for r in recipes if search_query.lower() in r["name"].lower()]
    return render_template_string(template, recipes=recipes)

@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipes = load_data()
        ingredients_list = request.form["ingredients"].splitlines()
        ingredients_dict = {}
        for item in ingredients_list:
            if "=" in item:
                name, qty = item.split("=", 1)
                ingredients_dict[name.strip()] = qty.strip()
        steps = request.form["steps"].splitlines()
        recipes.append({
            "name": request.form["name"],
            "ingredients": ingredients_dict,
            "steps": steps,
            "time": request.form["time"]
        })
        save_data(recipes)
        return redirect(url_for("home"))
    return render_template_string(add_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)