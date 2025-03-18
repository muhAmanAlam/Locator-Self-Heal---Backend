from bs4 import BeautifulSoup

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in ['path', 'svg', 'style', 'script', 'noscript']:
        for path in soup(tag):
            path.decompose()

    return str(soup)
