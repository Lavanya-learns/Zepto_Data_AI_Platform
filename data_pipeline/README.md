# Data Pipeline

This module collects book data from Books to Scrape, cleans the data, converts the prices, and stores the data in a SQLite database.

The pipeline contains 100 books collected from the first 5 pages of the website.

## What this module does

1. Scrapes book details from the website.
2. Cleans the scraped data.
3. Converts GBP prices to INR using the fixed rate of 1 GBP = 105.50 INR.
4. Stores the cleaned data in a normalized SQLite database.
5. Runs SQL queries on the database.
6. Reproduces a SQL JOIN using pandas `merge()`.

## Files

- `scrape_books.py` - Scrapes book details from the website.
- `clean_books.py` - Cleans the scraped data and converts prices.
- `create_database.py` - Creates the SQLite database and inserts the data.
- `queries.py` - Runs SQL queries and checks the pandas JOIN.
- `books_raw.csv` - Raw scraped data.
- `books_cleaned.csv` - Cleaned book data.
- `books.db` - SQLite database.
- `sql_outputs.txt` - Saved SQL query strings and their outputs.
- `requirements.txt` - Required Python packages.

## How to Run

Install the required packages:

```bash
pip install -r data_pipeline/requirements.txt

## Data Cleaning

The scraped price was originally stored as text, so the currency symbol was removed and the value was converted to a float.

Star ratings were given as words such as One, Two, Three, Four, and Five. These were converted to numbers from 1 to 5.

Availability was converted into a Boolean value:
- `True` if the book is in stock
- `False` otherwise

Price in INR was calculated using the fixed project rate:

`1 GBP = 105.50 INR`

The dataset was checked for missing values after cleaning. No missing values were found, so no imputation or row removal was required.

## Database Design

The data is stored in a SQLite database with two tables:

### Categories

Stores the category information.

- `category_id` - Primary key
- `category_name` - Category name

### Books

Stores the cleaned book information.

- `book_id` - Primary key
- `title` - Book title
- `price_gbp` - Price in GBP
- `price_inr` - Price converted to INR
- `rating` - Rating from 1 to 5
- `in_stock` - Whether the book is available
- `category_id` - Foreign key connected to the `categories` table

The `category_id` connects the two tables, so the category name can be obtained using a SQL JOIN.

## SQL Queries

Five SQL queries were used to practice different SQL operations:

1. **WHERE** - Find books with a rating of 5.
2. **ORDER BY and LIMIT** - Find the 5 most expensive books.
3. **DISTINCT** - Find the unique category IDs.
4. **BETWEEN** - Find books priced between £20 and £30.
5. **JOIN** - Combine books with their category names.

The query results were read into pandas using `pd.read_sql()`.

I also loaded the `books` and `categories` tables into pandas and used `pd.merge()` to reproduce the SQL JOIN. The results were compared using `.equals()`, which returned `True`.