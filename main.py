import httpx
from selectolax.lexbor import LexborHTMLParser
from urllib.parse import urljoin
from dataclasses import dataclass, asdict, fields
import csv
import html

@dataclass
class Item:
    name: str | None
    category: str | None
    price: str | None
    tax: str | None
    upc: str | None
    rating: int | None



def get_html(url, **kwargs):
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    if kwargs.get("page"):
        resp = httpx.get(
            url + str(kwargs.get("page")) + ".html", headers=headers
            )
    else:
        resp = httpx.get(url , headers=headers)
    
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page limit exceeded")
        return False

    html = LexborHTMLParser(resp.text)
    return html


# Creating a rating map since the outputs are written numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def parse_page(html):
    products = html.css("article.product_pod")

    page_url = "https://books.toscrape.com/catalogue/books/classics_6/index.html"

    for product in products:
        href = product.css_first("h3 a").attrs["href"]
        full_url = urljoin(page_url, href)
        yield full_url

def parse_item_page(html):
    #getting the rating number
    rating_class = html.css_first("p.star-rating").attrs["class"].split()[-1]
    rating_number = int(rating_map.get(rating_class))

    new_item = Item(
        name=extract_text(html, "div.product_main h1"),
        category=extract_text(html, "ul.breadcrumb li:nth-of-type(3)"),
        price=extract_text(html, "p.price_color"),
        tax= extract_text(html, "table.table-striped tr:nth-of-type(5) td"),
        upc= extract_text(html, "table.table-striped tr td"),
        rating= rating_number
    )
    return new_item

def extract_text(html, sel):
    try:
        text = html.css_first(sel).text(strip=True)
        return clean_data(text)
    except AttributeError:
        return None

def export_to_csv(products):
    field_names = [field.name for field in fields(Item)]
    with open("books.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows([asdict(p) for p in products])
    print("saved to csv")

def append_to_csv(products):
    field_names = [field.name for field in fields(Item)]
    with open("appendcsv.csv", "a") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writerows([asdict(p) for p in products])
    print("saved to appendcsv")

def clean_data(value):
    if value is None:
        return None

    value = value.replace("£", "")
    return value.strip()


def main():
    products = []
    baseurl = "https://books.toscrape.com/catalogue/category/books_1/page-"
    for x in range(1,10):
        print(f"Gettering page {x}")
        html = get_html(baseurl, page=x)
        if html is False:
            break
        product_urls = parse_page(html)
        for url in product_urls:
            print(url)
            html = get_html(url)
            products.append(parse_item_page(html))
    
    export_to_csv(products)


if __name__ == "__main__":
    main()