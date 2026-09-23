import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

all_books = []

for page in range(1, 6):
    url = base_url.format(page)

    response = requests.get(url)

    print("Page", page, "status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    print("Books found:", len(books))

    for book in books:
        title = book.h3.a["title"]

        price = book.find("p", class_="price_color").text.strip()

        rating_element = book.find("p", class_="star-rating")
        rating = rating_element.get("class")[1]

        availability = book.find(
            "p", class_="instock"
        ).text.strip()

        book_link = book.h3.a["href"]

        book_url = (
            "https://books.toscrape.com/catalogue/"
            + book_link.replace("../", "")
        )

        book_response = requests.get(book_url)

        book_soup = BeautifulSoup(book_response.text, "html.parser")

        category = (
            book_soup.find("ul", class_="breadcrumb")
            .find_all("li")[2]
            .text.strip()
        )

        book_data = {
            "title": title,
            "price": price,
            "star_rating": rating,
            "availability": availability,
            "category": category
        }

        all_books.append(book_data)

print("Total books collected:", len(all_books))

print("\nFirst book:")
print(all_books[0])

df = pd.DataFrame(all_books)

print("\nDataset shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())


df = pd.DataFrame(all_books)

df.to_csv("books_raw.csv", index=False)

print("Raw dataset saved successfully!")
