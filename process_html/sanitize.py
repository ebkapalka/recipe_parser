from urllib.parse import urlparse
from bs4 import BeautifulSoup
from copy import copy
import requests


def sanitize_html(url: str, tags: list[str] = None) -> BeautifulSoup:
    """
    God function to call separate sanitizing functions and return sanitized HTML
    :return:
    """
    if not tags:
        tags = ['style', 'script', 'link', 'a',
                'head', 'svg', 'footer', 'img']
    soup = get_soup(url)
    soup = remove_tags(soup, tags)
    soup = remove_attribs(soup)
    soup = remove_empty_tags(soup)
    soup = remove_sdivs(soup)

    lines = soup.prettify().split('\n')
    lines = [l.strip() for l in lines]
    return ''.join(lines)


def get_soup(url: str) -> BeautifulSoup:
    parsed_url = urlparse(url)
    if parsed_url.scheme in ['http', 'https']:
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
    else:
        with open(url, encoding='utf-8-sig') as f:
            soup = BeautifulSoup(f, "html.parser")
    return soup


def remove_tags(soup: BeautifulSoup, tags: list[str]):
    if 'a' in tags:
        for tag in soup.find_all('a'):
            tag.decompose()
        tags.remove('a')
    for elem in soup.find_all(tags):
        # Remove tags
        elem.decompose()
    return soup


def remove_attribs(soup: BeautifulSoup):
    for tag in soup.find_all(True):
        temp_tag = copy(tag)
        temp_tag.clear()
        if not temp_tag.get_text().strip():
            tag.attrs = {}
    return soup


def remove_sdivs(soup: BeautifulSoup):
    for tag in soup.find_all(['span', 'div']):
        if not tag.string or not tag.string.strip():
            tag.unwrap()
    return soup


def remove_empty_tags(soup: BeautifulSoup):
    empty_tags = soup.find_all(lambda x: not x.get_text().strip())
    while empty_tags:
        for tag in empty_tags:
            tag.decompose()
        empty_tags = soup.find_all(lambda x: not x.get_text().strip())
    return soup


def remove_a_tags(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.find_all('a'):
        tag.decompose()
    return soup

'''def remove_links(soup: BeautifulSoup):
    for tag in soup.find_all(href=True):
        del tag['href']
    for tag in soup.find_all(src=True):
        del tag['src']
    return soup


def remove_styles(soup: BeautifulSoup):
    for tag in soup.find_all(style=True):
        del tag['style']
    return soup'''


def remove_comments(soup: BeautifulSoup):
    return soup
