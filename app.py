import os
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template
import requests
import markdown
import sqlite3

db_connection = sqlite3.connect("./database.db")

db_cursor = db_connection.cursor()
db_cursor.execute(
    """
CREATE TABLE IF NOT EXISTS food (
    name TEXT,
    PRIMARY KEY (name)
)
"""
)
db_cursor.close()
db_connection.commit()

name = "Jack"

github_projects_url = "https://api.github.com/users/jackharrhy/repos"
projects_from_github = requests.get(github_projects_url).json()

projects = []
blog_posts = []

with os.scandir("blog") as it:
    for entry in it:
        if entry.name.endswith(".md") and entry.is_file():
            raw_post_date, post_name = entry.name.split("_")
            post_name = post_name.rstrip(".md")

            post_date = datetime.strptime(raw_post_date, "%Y-%m-%d")

            post_data = Path(entry.path).read_text()
            html = markdown.markdown(post_data)

            blog_posts.append({
                "name": post_name,
                "date": post_date,
                "html": html
            })

for project in projects_from_github:
    project_name = project["name"]
    desc = project["description"]
    url = project["html_url"]

    projects.append({
        "name": project_name,
        "desc": desc,
        "url": url,
    })

app = Flask(__name__)

@app.route("/")
def about_page():
    db_cursor = sqlite3.connect("./database.db").cursor()
    db_cursor.execute("SELECT * FROM food")
    list_of_food = db_cursor.fetchall()
    return render_template("about.html", name=name, list_of_food=list_of_food)

@app.route("/blog")
def blog_entry_page():
    return render_template("blog_listing.html", name=name, blog_posts=blog_posts)

@app.route("/blog/<post_name>")
def blog_listing_page(post_name):
    for post in blog_posts:
        if post_name == post["name"]:
            return render_template("blog_entry.html", name=name, post=post)

    return "Blog post not found"

@app.route("/projects")
def projects_page():
    return render_template("projects.html", name=name, projects=projects)

@app.route("/contact")
def contact_page():
    return render_template("contact.html", name=name)

@app.route("/food/add/<name>")
def add_food_page(name):
    db_connection = sqlite3.connect("./database.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT INTO food VALUES (:name)",
        {"name": name},
    )
    db_connection.commit()
    return f"Added food '{name}'"
