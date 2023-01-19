def tokenize_html(html: str, token_size: int = 4, max_len = 4000) -> list[str]:
    lines = html.split('\n')
    current_token = ''
    tokens = []
    for line in lines:
        temp_token = f"{current_token}\n{line}"
        if len(temp_token) <= max_len * token_size:
            current_token = temp_token
        else:
            tokens.append(current_token)
            current_token = line
    if current_token:
        tokens.append(current_token)
    return tokens
