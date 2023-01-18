from process_html.sanitize import sanitize_html
import openai

if __name__ == '__main__':
    recipe_url = "https://www.joshuaweissman.com/post/" \
                 "the-easiest-noodle-dish-ever-yaki-udon"
    print(sanitize_html(recipe_url).prettify())
