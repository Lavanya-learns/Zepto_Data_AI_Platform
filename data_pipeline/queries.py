import sqlite3
import pandas as pd

# Save query results to a text file
output_file = open("sql_outputs.txt", "w", encoding="utf-8")

# Connect to the database
connection = sqlite3.connect("books.db")

# Query 1: Find books with a rating of 5
query1 = """
SELECT title, rating
FROM books
WHERE rating = 5
"""

result1 = pd.read_sql(query1, connection)

print("Query 1: Books with a rating of 5")
print(result1)

output_file.write("Query 1: Books with a rating of 5\n")
output_file.write(query1)
output_file.write("\n\n")
output_file.write(result1.to_string())
output_file.write("\n\n")

# Query 2: Find the 5 most expensive books
query2 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 5
"""

result2 = pd.read_sql(query2, connection)

print("\nQuery 2: 5 Most Expensive Books")
print(result2)

output_file.write("Query 2: 5 Most Expensive Books\n")
output_file.write(query2)
output_file.write("\n\n")
output_file.write(result2.to_string())
output_file.write("\n\n")

# Query 3: Find all unique categories
query3 = """
SELECT DISTINCT category_id
FROM books
"""

result3 = pd.read_sql(query3, connection)

print("\nQuery 3: Unique Category IDs")
print(result3)

output_file.write("Query 3: Unique Category IDs\n")
output_file.write(query3)
output_file.write("\n\n")
output_file.write(result3.to_string())
output_file.write("\n\n")

# Query 4: Find books priced between £20 and £30
query4 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 30
ORDER BY price_gbp
"""

result4 = pd.read_sql(query4, connection)

print("\nQuery 4: Books priced between £20 and £30")
print(result4)

output_file.write("Query 4: Books priced between £20 and £30\n")
output_file.write(query4)
output_file.write("\n\n")
output_file.write(result4.to_string())
output_file.write("\n\n")

# Query 5: Join books with their categories
query5 = """
SELECT books.title, books.price_gbp, categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
LIMIT 10
"""

result5 = pd.read_sql(query5, connection)

print("\nQuery 5: Books with their categories")
print(result5)

output_file.write("Query 5: Books with their categories\n")
output_file.write(query5)
output_file.write("\n\n")
output_file.write(result5.to_string())
output_file.write("\n\n")

# Read both tables into pandas DataFrames
books_df = pd.read_sql("SELECT * FROM books", connection)
categories_df = pd.read_sql("SELECT * FROM categories", connection)

# Reproduce the SQL JOIN using pandas merge
merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

print("\nPandas JOIN using merge:")
print(merged_df[["title", "price_gbp", "category_name"]].head(10))

# Check that SQL JOIN and pandas merge give the same result
sql_join = result5[["title", "price_gbp",
                    "category_name"]].reset_index(drop=True)

pandas_join = merged_df[
    ["title", "price_gbp", "category_name"]
].head(10).reset_index(drop=True)

print("\nSQL JOIN and pandas merge match:")
print(sql_join.equals(pandas_join))

# Close the output file
output_file.close()

# Close the database connection
connection.close()
