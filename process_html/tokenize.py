class PromptGenerator:
    def __init__(self, html: str, max_tokens: int, return_tokens: int = 500, initial_prompt: str = None):
        """
        Object that serves the next set of tokens without exceeding the max total
        :param html: html document, as a string
        :param max_tokens: total number of allowable tokens for prompt tokens + response tokens
        :param return_tokens: the number of tokens requested to return
        :param initial_prompt: the question that precedes the first batch of tokens
        """

        self.html = [line.strip() for line in html.split('\n')]
        self.max_tokens = max_tokens
        self.return_tokens = return_tokens
        self.initial_prompt = initial_prompt

        if not self.initial_prompt:
            self.initial_prompt = ("The following HTML contains a recipe.  Isolate the "
                                   "list of ingredients (with quantities) and the " +
                                   "steps to create the food and return them as two lists:  ")

    def get_max_prompt(self) -> str:
        prompt = self.initial_prompt
        for line in self.html:
            temp_prompt = f"{prompt}\n{line}"
            if len(temp_prompt) <= self.max_tokens - self.return_tokens:
                prompt = temp_prompt
            else:
                break
        return prompt
