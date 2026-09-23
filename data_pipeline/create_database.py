import sqlite3
import pandas as pd

# Read the cleaned book data
df = pd.read_csv("books_cleaned.csv")

print("Cleaned dataset loaded:", df.shape)

# Create a SQLite database
connection = sqlite3.connect("books.db")

print("Database connection created!")

# Create the categories table
connection.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE NOT NULL
)
""")

print("Categories table created!")

# Get unique categories from the dataset
categories = df["category"].drop_duplicates().reset_index(drop=True)

# Insert each category into the categories table
for category in categories:
    connection.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        (category,)
    )

connection.commit()

print("Categories inserted:", len(categories))

# Create the books table
connection.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock BOOLEAN,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")

connection.commit()

print("Books table created!")

# Clear old book records before inserting fresh data
connection.execute("DELETE FROM books")

# Insert books into the books table
for _, row in df.iterrows():
    category_id = connection.execute(
        "SELECT category_id FROM categories WHERE category_name = ?",
        (row["category"],)
    ).fetchone()[0]

    connection.execute(
        """
        INSERT INTO books
        (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            row["in_stock"],
            category_id
        )
    )

connection.commit()

print("Books inserted:", len(df))

# Check the number of rows in each table
category_count = connection.execute(
    "SELECT COUNT(*) FROM categories"
).fetchone()[0]

book_count = connection.execute(
    "SELECT COUNT(*) FROM books"
).fetchone()[0]

print("Categories in database:", category_count)
print("Books in database:", book_count)

# Close the database connection
connection.close()

print("Database connection closed!")
