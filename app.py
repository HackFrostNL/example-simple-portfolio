from flask import Flask, render_template
import requests

name = "Jack"

github_projects_url = "https://api.github.com/users/jackharrhy/repos"
projects_from_github = requests.get(github_projects_url).json()

projects = []

for project in projects_from_github:
    name = project["name"]
    desc = project["description"]
    url = project["html_url"]

    projects.append({
        "name": name,
        "desc": desc,
        "url": url,
    })

list_of_food = [
    "Tea",
    "Apples",
    "Ramen"
]

app = Flask(__name__)

@app.route("/")
def about_page():
    return render_template("about.html", name=name, list_of_food=list_of_food)

@app.route("/projects")
def projects_page():
    return render_template("projects.html", name=name, projects=projects)

@app.route("/contact")
def contact_page():
    return render_template("contact.html", name=name)
