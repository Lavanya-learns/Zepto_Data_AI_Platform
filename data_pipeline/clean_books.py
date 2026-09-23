import pandas as pd

# Read the raw scraped data
df = pd.read_csv("books_raw.csv")

print("Original dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Convert price from text to a number
df["price_gbp"] = (
    df["price"]
    .str.replace("Â£", "", regex=False)
    .astype(float)
)

print("\nPrice after cleaning:")
print(df[["price", "price_gbp"]].head())

# Convert star ratings from words to numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["star_rating"].map(rating_map)

print("\nRating after cleaning:")
print(df[["star_rating", "rating"]].head())

# Convert availability to True or False
df["in_stock"] = df["availability"].str.contains("In stock", case=False)

print("\nAvailability after cleaning:")
print(df[["availability", "in_stock"]].head())

# Convert GBP price to INR using the required fixed rate
GBP_TO_INR = 105.50

df["price_inr"] = df["price_gbp"] * GBP_TO_INR

print("\nPrice in INR:")
print(df[["price_gbp", "price_inr"]].head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Save the cleaned dataset
df.to_csv("books_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Final shape:", df.shape)
