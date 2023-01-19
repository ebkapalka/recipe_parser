from bs4 import BeautifulSoup, Comment
import requests


def sanitize_html(url: str, rem_tags: list[str] = None) -> BeautifulSoup:
    """
    God function to call separate sanitizing functions and return sanitized HTML
    :param url: the URL path to the page to be sanitized
    :param rem_tags: HTML tags to remove
    :param keep_attribs: HTML attributes to retain
    :return: BeautifulSoup object with extraneous data removed
    """

    if not rem_tags:
        rem_tags = ['style', 'script', 'link', 'path',
                    'svg', 'head', 'header', 'img',
                    'footer', 'button', 'label']
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    '''soup = remove_specific_tags(soup, rem_tags)
    soup = remove_empty_tags(soup)
    soup = remove_attributes(soup)
    soup = remove_styling_tags(soup)

    soup = remove_comments(soup)
    return soup'''

    for elem in soup(['style', 'script']):
        # Remove tags
        elem.decompose()
    for tag in soup.find_all():
        if not list(tag.stripped_strings):
            tag.extract()
    print(soup.prettify())


def remove_specific_tags(soup: BeautifulSoup, tags: list[str]) -> BeautifulSoup:
    """
    Iterates through elements matching any tag in the provided list and removes them
    :param soup: HTML data, as a BeautifulSoup object
    :param tags: tags of elements to remove
    :return: BeautifulSoup object with extraneous data removed
    """
    for elem in soup(tags):
        # Remove rem_tags
        elem.decompose()
    return soup


def remove_empty_tags(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove tags with no enclosed text
    :param soup: HTML data, as a BeautifulSoup object
    :return: BeautifulSoup object with extraneous data removed
    """
    while True:
        empty_tags = []
        for elem in soup.find_all(True):
            if not elem.text.strip():
                empty_tags.append(elem)
        if not empty_tags:
            break
        for elem in empty_tags:
            elem.decompose()
    return soup


def remove_styling_tags(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove extra nested Div and Span tags
    :param soup: HTML data, as a BeautifulSoup object
    :return: BeautifulSoup object with extraneous data removed
    """

    divs = soup.find_all(['div', 'span'])
    for div in divs[1:]:
        div.unwrap()
    return soup


def remove_comments(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove comments from HTML
    :param soup: HTML data, as a BeautifulSoup object
    :return: BeautifulSoup object with extraneous data removed
    """

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return soup


def remove_attributes(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove attributes from elements to simplify and reduce character count
    :param soup: HTML data, as a BeautifulSoup object
    :param keep_attribs: list of attributes to retain (default None)
    :return: BeautifulSoup object with extraneous data removed
    """

    for element in soup.find_all():
        element.attrs = {}
    return soup
