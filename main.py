from process_html.sanitize import sanitize_html
from process_html.tokenize import tokenize_html
from load_file import load_secrets
import openai

if __name__ == '__main__':
    # recipe_url = "https://www.joshuaweissman.com/post/" \
    #              "the-easiest-noodle-dish-ever-yaki-udon"
    recipe_url = "https://www.justonecookbook.com/pickled-ginger/"
    html = sanitize_html(recipe_url).prettify()
    html_chunks = tokenize_html(html, prompt_length=1000)
    secrets = load_secrets("secrets.json")
    openai.api_key = secrets.get("OpenAI API Key", "Not Found")

    total_tokens = sum(len(t) for t in html_chunks)
    print(f"Number of prompts: {len(html_chunks)}")
    print(f'Longest prompt: {len(max(html_chunks, key=len))}')
    print(f"Average prompt: {int(total_tokens/len(html_chunks))}")
    print(f'Total Tokens: {total_tokens}')
    results = []
    for i, chunk in enumerate(html_chunks):
        if i == 0:
            prompt = f"The following HTML is from a webpage containing a recipe.  It may be" \
                     f"sent to you in chunks depending on how large the page is.  Isolate the " \
                     f"list of ingredients from the following HTML if present and return them" \
                     f"in a bulleted list.  Do not return HTML tags -- if you do not clearly" \
                     f"recognize a list of ingredients, return an empty string: {chunk}"
        else:
            prompt = f"Continued from above -- This list may or may not contain part of " \
                     f"or the entirety list of ingredients.  If it does not clearly contain" \
                     f"a list of ingredients, return an empty string.  Do not return HTML: {chunk}"
        print(f"Prompt Length with preamble: {len(prompt)}")
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,    # this is for the RESPONSE
            n=1,
            stop=None,
            temperature=0.5,
        )
        result = completions.choices[0].text
        print(result, "\n\n||||\n\n")
