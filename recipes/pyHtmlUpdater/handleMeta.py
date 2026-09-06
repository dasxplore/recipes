import re
import yaml
import os
from bs4 import BeautifulSoup
from pathlib import Path

# global vars
base_path = Path(__file__).resolve().parent.parent

FRONT_MATTER_RE = re.compile(
    r"^---[ \t]*\r?\n(.*?\r?\n)(?:---|\.\.\.)[ \t]*\r?\n",
    re.DOTALL
)

# Global functions

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


## Run it ##

metas = ["keywords"]
meta_ogs = ["og:image", "og:title", "og:description", "og:url"]
mkdocs_path = base_path / "mkdocs.yml"
docs_path = base_path / "docs"
site_path = base_path / "site"
print(f"site_path: {site_path}")

# get the nav details from mkdocs configuration
with open(mkdocs_path, "r") as f:
    mkdocs = yaml.safe_load(f)

paths = get_file_paths(mkdocs["nav"])

for path in paths:
    md_path = docs_path / path
    html_path = site_path / path
    html_path = html_path.with_suffix(".html")

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        front_matter = get_meta_tags(md_path)
        if front_matter:
            # for each require meta tags
            for mt in metas:
                mt_val = front_matter.get(mt, None)
                if mt_val:
                    set_meta(soup, mt, mt_val)
            # for each og meta tags
            for og in meta_ogs:
                og_val = front_matter.get(og, None)
                if og_val:
                    set_meta_property(soup, og, og_val)
        # beautify the html
        html = soup.prettify(formatter="html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Finished updating: {html_path}")

# End