import json


def load_secrets(path: str) -> dict:
    """
    Loads a JSON file containing the API key
    :param path: relative or absolute file path to JSON file
    :return: dict of JSON data or empty dict
    """
    try:
        with open(path) as f:
            data = f.read()
            return json.loads(data)
    except Exception as e:
        print(e)
        return {}
