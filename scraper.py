import requests
from bs4 import BeautifulSoup
import csv
import re


def clean_description(description):
    description = re.sub(r'<br\s?/?>', ' ', description)
    description = re.sub(r'\n+', '\n', description).strip()
    return description


def extract_author(author_text):
    return author_text.replace("Nama Author: ", "").strip()


def scrape_novel_detail(detail_url):
    response = requests.get(detail_url)
    if not response.ok:
        return "Author not found", "Description not found", "Rating not found"

    detail_soup = BeautifulSoup(response.content, 'html.parser')
    author_elem = detail_soup.find('p', class_='detail-author web-author')
    author = extract_author(author_elem.text.strip()
                            ) if author_elem else "Author not found"
    print(author)

    description_div = detail_soup.find('div', class_='detail-desc')
    description = clean_description(description_div.find(
        'p').decode_contents()) if description_div else "Description not found"

    rating_elem = detail_soup.find('div', class_='detail-score').find('span')
    rating = rating_elem.text if rating_elem else "Rating not found"
    print(rating)
    print("===")

    return author, description, rating


def scrape_novel_page(page_num):
    base_url = 'https://noveltoon.mobi/id/genre/novel?page={}'
    url = base_url.format(page_num)

    response = requests.get(url)
    if not response.ok:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    novels = soup.find_all('a', class_='genre-item-box')

    novel_data = []

    for novel in novels:
        title = novel.find('p', class_='genre-item-title').text.strip()
        print(title)
        genre = novel.find('span', class_='genre-item-label').text.strip()
        detail_url = novel['href']

        cover_url = novel.find(
            'div', class_='genre-item-image').find('img')['src']

        author, description, rating = scrape_novel_detail(detail_url)

        novel_data.append([title, description, genre, author,
                          rating, cover_url, detail_url])

    return novel_data


def main():
    with open('novel_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "Genre",
                        "Author", "Rating", "Cover", "Detail"])

        for page_num in range(1, 51):
            page_data = scrape_novel_page(page_num)
            writer.writerows(page_data)
            print(f"Scraped page {page_num} out of 51")

    print("Scraping completed and data saved to novel_data.csv")


if __name__ == "__main__":
    main()
