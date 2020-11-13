import requests
from bs4 import BeautifulSoup as bs


def has_article_contains(article_link: str, keywords: list):
    """This function gets title, text, tags and hubs of article and finds keywords in it

    Args:
        article_link (str): web link of article
        keywords (list): keywords (search words)

    Returns:
        [bool]: True if though one of keywords was found
                False if wasn't found
    """
    ret = requests.get(article_link)
    soup = bs(ret.text, 'html.parser')
    article = soup.find('article', class_='post post_full')

    text = list()
    text.append(article.find(
        'span', class_='post__title-text').text.lower())
    text.append(article.find(
        'div', class_='post__text').text.lower())

    tags = article.find_all('a', class_='inline-list__item-link post__tag')
    tag_text = list([t.text for t in tags])
    text.extend(tag_text)

    for keyword in keywords:
        for item in text:
            if str(item).find(keyword) >= 0:
                return True
    return False


def main():
    """This function finds keywords into full text articles represent on the main habr.com page
    """
    KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'capcom']
    # KEYWORDS = ['с помощью alerta.io']

    ret = requests.get("https://habr.com/ru/all/")
    soup = bs(ret.text, 'html.parser')

    all_articles = soup.find_all('article', class_="post post_preview")
    for article in all_articles:
        article_link = article.find("a", class_="btn").attrs.get('href')
        if has_article_contains(article_link, KEYWORDS):
            article_title = article.find(
                "h2", class_="post__title").text.replace('\n', '')
            article_time = article.find(
                "span", class_="post__time").text.replace('\n', '')
            print(f"{article_time} - {article_title} - {article_link}")


if __name__ == "__main__":
    main()
