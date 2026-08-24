import re
import yaml
from bs4 import BeautifulSoup

FRONT_MATTER_RE = re.compile(
    r"^---[ \t]*\r?\n(.*?\r?\n)(?:---|\.\.\.)[ \t]*\r?\n",
    re.DOTALL
)

def get_meta_tags(md_file:str) -> dict | None :
    front_matter = None
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = FRONT_MATTER_RE.match(content)
    if match:
        front_matter = yaml.safe_load(match.group(1))
    return front_matter


def get_file_paths(obj):
    paths = []

    if isinstance(obj, dict):
        for value in obj.values():
            paths.extend(get_file_paths(value))

    elif isinstance(obj, list):
        for item in obj:
            paths.extend(get_file_paths(item))

    elif isinstance(obj, str):
        if obj.endswith(".md"):
            paths.append(obj)

    return paths

def set_meta(soup, name, content):
    meta = soup.head.find("meta", attrs={"name": name})

    if meta is None:
        meta = soup.new_tag("meta")
        meta["name"] = name
        soup.head.append(meta)

    meta["content"] = content

def set_meta_property(soup, prop, content):
    meta = soup.head.find("meta", attrs={"property": prop})

    if meta is None:
        meta = soup.new_tag("meta")
        meta["property"] = prop
        soup.head.append(meta)

    meta["content"] = content

## Run it

with open("../mkdocs.yml", "r") as f:
    mkdocs = yaml.safe_load(f)

paths = get_file_paths(mkdocs["nav"])
print(paths)

html_file = "index.html" # will be in loop
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

set_meta(
    soup,
    "keywords",
    "indian recipes, healthy recipe, easy veg recipe, easy non veg recipe"
)

set_meta_property(soup, "og:title", "Chicken Recipe")

# Beautify
html = soup.prettify(formatter="html")

# Save the final output
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

