# Books to Scrape Scraper

This project is part of my portfolio and demonstrates my ability to build a complete web scraping pipeline in Python. It targets [Books to Scrape](https://books.toscrape.com), a site designed for scraping practice, and extracts structured book data into a CSV file.

## Project Overview

The scraper navigates through category pages, follows product links, and extracts details about each book. It uses `httpx` for HTTP requests and `selectolax` for efficient HTML parsing. Data is modeled with Python dataclasses to keep the code clean and maintainable, and exported to CSV for analysis.

## Data Collected

The scraper extracts the following fields for each book:

* Title  
* Category  
* Price  
* Tax  
* UPC  
* Rating (converted from words like “Three” into integers)

## Technical Highlights

* Built with Python 3.10+  
* Uses `httpx` for fast and reliable HTTP requests  
* Parses HTML with `selectolax`, a high‑performance parser  
* Models data with `dataclasses` for clarity and type safety  
* Cleans raw text with helper functions to normalize values  
* Exports results with `csv.DictWriter` using `asdict()` for dataclass conversion  

## Why This Project Matters

This scraper shows my ability to:

* Work with HTTP requests and headers  
* Parse and navigate HTML structures  
* Transform raw data into clean, structured formats  
* Apply Python features like dataclasses and helper functions  
* Handle file export and data persistence  

