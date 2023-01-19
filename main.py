from process_html.sanitize import sanitize_html
from process_html.tokenize import PromptGenerator
from load_file import load_secrets
import openai

MODELS = {
    "text-davinci-003": {"Model": "GPT-3", "Max Request": 4000},
    "text-curie-001": {"Model": "GPT-3", "Max Request": 2048},
    "text-babbage-001": {"Model": "GPT-3", "Max Request": 2048},
    "text-ada-001": {"Model": "GPT-3", "Max Request": 2048},
    "code-davinci-002": {"Model": "Codex", "Max Request": 8000},
    "code-cushman-001": {"Model": "Codex", "Max Request": 2048}
}

if __name__ == '__main__':
    recipe_url = "https://www.justonecookbook.com/pickled-ginger/"
    return_token_size: int = 500
    gpt_model = "text-davinci-003"

    html = sanitize_html(recipe_url).prettify()
    print(html)
    secrets = load_secrets("secrets.json")
    openai.api_key = secrets.get("OpenAI API Key", None)
    prompt_generator = PromptGenerator(html, max_tokens=MODELS[gpt_model]["Max Request"],
                                       return_tokens=return_token_size)
    prompt = prompt_generator.get_max_prompt()
    print(prompt)
    '''completions = openai.Completion.create(
        engine=gpt_model,
        prompt=prompt,
        max_tokens=return_token_size,  # this is for the RESPONSE
        n=1, stop=None,
        temperature=0.5,
    )
    result = completions.choices[0].text
    print(result)'''
