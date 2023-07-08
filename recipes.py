from recipe_scrapers import scrape_me
import urllib.request
import unicodedata
import re
import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

recipe_url = sys.argv[1]

scraper = scrape_me(recipe_url, wild_mode=True)

recipe_json = scraper.to_json()

title = recipe_json["title"]
total_time = recipe_json["total_time"]
servings = re.sub("[^0-9]", "", recipe_json["yields"])
host = recipe_json["host"]
site_name = recipe_json["site_name"]

ingredients_list = recipe_json["ingredients"]
ingredients = ""
for i, v in enumerate(ingredients_list):
    ingredients += f"   - {v}\n"

instructions_list = recipe_json["instructions_list"]
instructions = ""
for i, v in enumerate(instructions_list):
    instructions += f"{i + 1}. {v}\n\n"

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

image_url = recipe_json["image"]

image_path = "/img/recipes/"
image_name = slugify(title) + "." + image_url.split('.')[-1]

def download_jpg(url, file_path, file_name):
    full_path = file_path + file_name + "." + url.split('.')[-1]
    urllib.request.urlretrieve(url, full_path)

def recipesConcat():
    return (
        f'---\n'
        f'title: {title}\n'
        f'image: {image_path}{image_name}\n'
        f'tags: \n'
        f'time: {total_time} min\n'
        f'servings: {servings}\n'
        f'sourceLabel: {site_name}\n'
        f'sourceURL: {recipe_url}\n'
        f'ingredients: \n'
        f'{ingredients}'
        f'---\n'
        f'{instructions}'
    )

f = open(f"src/recipes/{slugify(title)}.md", "w")
f.write(recipesConcat())
f.close()

download_jpg(image_url, r".\src\img\recipes/", slugify(title) )