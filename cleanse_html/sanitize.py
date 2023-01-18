from bs4 import BeautifulSoup, Comment
import requests


def sanitize_html(url: str, rem_tags: list[str] = None, keep_attribs: list[str] = None) -> BeautifulSoup:
    """
    God function to call separate sanitizing functions and return sanitized HTML
    :param url: the URL path to the page to be sanitized
    :param rem_tags: HTML tags to remove
    :param keep_attribs: HTML attributes to retain
    :return: BeautifulSoup object with extraneous data removed
    """

    if not rem_tags:
        rem_tags = ['style', 'script', 'link',
                'path', 'svg', 'head', 'img']
    if not keep_attribs:
        keep_attribs = ['']
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    soup = remove_specific_tags(soup, rem_tags)
    soup = remove_attributes(soup, keep_attribs)
    soup = remove_empty_tags(soup)
    soup = remove_styling_tags(soup)
    soup = remove_comments(soup)
    return soup


def remove_specific_tags(soup: BeautifulSoup, tags: list[str]) -> BeautifulSoup:
    """
    Iterates through elements matching any tag in the provided list and removes them
    :param soup: HTML data, as a BeautifulSoup object
    :param tags:
    :return:
    """
    for data in soup(tags):
        # Remove rem_tags
        data.extract()
    return soup


def remove_empty_tags(soup: BeautifulSoup) -> BeautifulSoup:
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
    divs = soup.find_all(['div', 'span'])
    for div in divs[1:]:
        div.unwrap()
    return soup


def remove_comments(soup: BeautifulSoup) -> BeautifulSoup:
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return soup


def remove_attributes(soup: BeautifulSoup, keep_attribs: list[str]) -> BeautifulSoup:
    for element in soup.find_all():
        temp_attrs = element.attrs.copy()
        for attribute in element.attrs:
            if attribute not in keep_attribs:
                del temp_attrs[attribute]
        element.attrs = temp_attrs
    return soup