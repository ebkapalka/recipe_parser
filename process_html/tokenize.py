# TODO: make this into a generator so it can take one set of information at a time
def tokenize_html(html: str, prompt_length: int = 250, max_tokens: int = 4000) -> list[str]:
    lines = html.split('\n')
    current_token = ''
    tokens = []
    for line in lines:
        temp_token = f"{current_token}\n{line.strip()}"
        if len(temp_token) < max_tokens - prompt_length:
            current_token = temp_token
        else:
            tokens.append(current_token)
            current_token = line.strip()
    if current_token:
        tokens.append(current_token)
    return tokens
