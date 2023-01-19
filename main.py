from process_html.sanitize import sanitize_html
from process_html.tokenize import tokenize_html
from load_file import load_secrets
import openai

if __name__ == '__main__':
    recipe_url = "https://www.joshuaweissman.com/post/" \
                 "the-easiest-noodle-dish-ever-yaki-udon"
    html = sanitize_html(recipe_url).prettify()
    tokens = tokenize_html(html)
    secrets = load_secrets("secrets.json")
    openai.api_key = secrets.get("OpenAI API Key", "Not Found")
    print(tokens[0].__repr__())