# Zepto Data & AI Platform

An end-to-end data and AI platform built with Python, covering data collection and processing, exploratory data analysis, machine learning, and a RAG-based customer support assistant.

# Project Overview

This project contains three integrated modules:

1. **Data Pipeline** — Web scraping, data cleaning, SQLite database creation, SQL analysis, and Pandas validation.
2. **Analytics & Machine Learning** — Titanic dataset EDA, classification, imbalance handling, hyperparameter tuning, and regression.
3. **Support Assistant** — Retrieval-Augmented Generation (RAG) using Sentence Transformers, ChromaDB, LangGraph, Pydantic, and FastAPI.

# Project Structure

# text
Zepto_Data_AI_Platform/
│
├── README.md
│
├── data_pipeline/
│   ├── scrape_books.py
│   ├── clean_books.py
│   ├── create_database.py
│   ├── queries.py
│   ├── books_raw.csv
│   ├── books_cleaned.csv
│   ├── books.db
│   ├── sql_outputs.txt
│   ├── requirements.txt
│   └── README.md
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── best_titanic_pipeline.joblib
│   └── README.md
│
└── support_assistant/
    ├── main.py
    ├── requirements.txt
    ├── Dockerfile
    ├── README.md
    └── docs/
        ├── doc_01.txt
        ├── doc_02.txt
        ├── doc_03.txt
        ├── doc_04.txt
        ├── doc_05.txt
        ├── doc_06.txt
        ├── doc_07.txt
        └── doc_08.txt
```

# Requirements and Setup

The project uses **module-level requirements files**.

# Data Pipeline
Install:
```bash
pip install -r data_pipeline/requirements.txt
```

# Main technologies:
* Python
* Requests
* BeautifulSoup
* Pandas
* SQLite

# Analytics
The analytics notebooks use:
* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Imbalanced-learn
* Joblib

Open the notebooks using Jupyter Notebook, JupyterLab, or VS Code.

# Support Assistant
Install:
```bash
pip install -r support_assistant/requirements.txt
```

# Main technologies:
* FastAPI
* Uvicorn
* Sentence Transformers
* ChromaDB
* LangGraph
* Pydantic
* NumPy

# Module 1 — Data Pipeline

## Workflow
The data pipeline:
1. Scrapes book information from Books to Scrape using Requests and BeautifulSoup.
2. Collects title, price, rating, availability, and category.
3. Cleans and converts the scraped values into analysis-ready formats.
4. Converts GBP prices to INR using the fixed rate:

```text
1 GBP = 105.50 INR
```
Stores the cleaned data in a normalized SQLite database.
Runs SQL queries using filtering, sorting, limiting, distinct values, ranges, and joins.
Reproduces database results using Pandas and validates SQL joins using pd.merge().

# Run
From the data_pipeline directory:
python scrape_books.py
python clean_books.py
python create_database.py
python queries.py
The generated database and SQL outputs are included in the repository.

# Design Decision
SQLite was selected because it provides a lightweight relational database without requiring a separate database server. The pipeline separates scraping, cleaning, database creation, and querying into different scripts to keep each stage clear and reusable.
 Stores the cleaned data in a normalized SQLite database.
 Runs SQL queries using filtering, sorting, limiting, distinct values, ranges, and joins.
 Reproduces database results using Pandas and validates SQL joins using pd.merge().
 
# Run
From the data_pipeline directory:
python scrape_books.py
python clean_books.py
python create_database.py
python queries.py
The generated database and SQL outputs are included in the repository.

# Design Decision
SQLite was selected because it provides a lightweight relational database without requiring a separate database server. The pipeline separates scraping, cleaning, database creation, and querying into different scripts to keep each stage clear and reusable.

# Module 2 — Analytics & Machine Learning
Workflow

# The analytics module:
Loads the Titanic dataset.
Saves the original dataset as titanic.csv.
Performs exploratory data analysis and missing-value analysis.
Handles missing values according to the specified percentage thresholds.
Performs univariate and multivariate analysis.
Analyzes survival patterns by sex and passenger class.
Builds the required correlation matrix.
Compares Logistic Regression, Decision Tree, and Random Forest models.
Evaluates class imbalance strategies.
Uses GridSearchCV for Random Forest tuning.
Builds a regression model to predict fare.
Evaluates classification and regression performance.
Saves the complete fitted classification pipeline using Joblib.
Reloads the saved pipeline and demonstrates prediction on raw input.

# Run
Open and run the notebooks in this order:
analytics/01_eda.ipynb
analytics/02_modeling.ipynb
The saved dataset and trained pipeline are included in the repository.

# Design Decision
The analytics workflow separates EDA from modeling so that data understanding and model development remain organized. Scikit-learn Pipelines and ColumnTransformer are used to keep preprocessing consistent and prevent data leakage during model training.

# Module 3 — Zepto Support Assistant
Workflow

# The support assistant follows a RAG architecture:
Policy Documents
      ↓
Document Loading
      ↓
Sentence Transformer Embeddings
      ↓
ChromaDB
      ↓
User Query
      ↓
Intent Classification
      ↓
Retrieval of Top 3 Documents
      ↓
Answer Generation
      ↓
Pydantic Validation
      ↓
FastAPI Response

# The assistant contains three LangGraph nodes:
classify_intent
retrieve_and_answer
direct_answer

Policy-related questions are routed through retrieval, while unsupported general questions receive a direct response.

The default configuration uses mock LLM behavior so that the project can run without paid APIs or API keys.

# Run
From the support_assistant directory:
python main.py
To start the FastAPI application:
uvicorn main:app --reload
The API endpoint is:
POST /ask

# Example request:
{
  "query": "How much does standard delivery cost?"
}

# Example general question:
{
  "query": "What is the capital of India?"
}

# Docker
Build the image:
docker build -t zepto-support-assistant .
Run the container:
docker run -p 8000:8000 zepto-support-assistant

# Design Decision
Sentence Transformers provides local semantic embeddings, while ChromaDB stores and retrieves document vectors using cosine similarity. LangGraph was used to make the assistant workflow explicit and modular. FastAPI provides a lightweight API interface, and Pydantic validates the final response structure.

# Key Design Principles
Modular Python scripts and notebooks
Reproducible data processing
Relational database design for structured data
Prevention of data leakage during machine learning
Reusable fitted ML pipeline
Local semantic retrieval using embeddings
Explicit LangGraph workflow
Structured API responses using Pydantic
No paid external services required

# Academic Integrity
All modules are organized as reproducible project work with source code, datasets, notebooks, outputs, and documentation included where required by the project specification.

## Project Status
All three modules are organized in the repository with their source code, documentation, outputs, and required project files.
