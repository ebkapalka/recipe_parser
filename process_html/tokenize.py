class PromptGenerator:
    def __init__(self, html: str, max_tokens: int, return_tokens: int = 500,
                 initial_prompt: str = None, successive_prompt: str = None):
        """
        Object that serves the next set of tokens without exceeding the max total
        :param html: html document, as a string
        :param max_tokens: total number of allowable tokens for prompt tokens + response tokens
        :param return_tokens: the number of tokens requested to return
        :param initial_prompt: the question that precedes the first batch of tokens
        :param successive_prompt: the question that precedes successive batches of tokens
        """

        self.html = [line.strip() for line in html.split('\n')]
        self.max_tokens = max_tokens
        self.return_tokens = return_tokens
        self.initial_prompt = initial_prompt
        self.successive_prompt = successive_prompt
        self.index = 0

        if not self.initial_prompt:
            self.initial_prompt = ("The following HTML is from a webpage containing " +
                                   "a recipe.  It may be sent to you in chunks " +
                                   "depending on how large the page is.  Isolate the " +
                                   "list of ingredients from the following HTML if " +
                                   "present and return them in a bulleted list.  Do not " +
                                   "return HTML tags -- if you do not clearly recognize " +
                                   "a list of ingredients, return an empty string: ")
        if not self.successive_prompt:
            self.successive_prompt = ("Continued from above -- This list may or may not " +
                                      "contain part of or the entirety list of " +
                                      "ingredients.  If it does not clearly contain a list " +
                                      "of ingredients, return an empty string.  Do not " +
                                      "return HTML: ")

    def get_max_prompt(self) -> str:
        prompt = self.initial_prompt
        for line in self.html:
            temp_prompt = f"{prompt}\n{line}"
            if len(temp_prompt) <= self.max_tokens - self.return_tokens:
                prompt = temp_prompt
            else:
                break
        return prompt

    def get_next_prompt(self) -> str:
        """
        Retrieve the next prompt while respecting the maximum size, return size, and preamble size.
        This is based on a flawed understanding od GPT's "context", which is not the maximum amount
        of information you can transact at one time, but the maximum amount of information the model
        can interact with at one time.  This code is staying in for future reference
        :return: the largest possible prompt without going over the size limit
        """
        current_prompt = self.initial_prompt if self.index == 0 else self.successive_prompt
        if self.index >= len(self.html):
            # case where there are no remaining lines of HTML
            return ''
        while self.index < len(self.html):
            temp_prompt = f"{current_prompt}\n{self.html[self.index]}"
            if len(temp_prompt) <= self.max_tokens - self.return_tokens:
                current_prompt = temp_prompt
                self.index += 1
            else:
                return current_prompt
        return current_prompt
