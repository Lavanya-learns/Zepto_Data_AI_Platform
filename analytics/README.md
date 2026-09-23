# Titanic Data Analysis and Machine Learning

## Overview

This project analyzes the Titanic dataset to understand the factors associated with passenger survival and to build machine learning models for classification and fare prediction.

The project includes:

* Exploratory Data Analysis (EDA)
* Data cleaning and preprocessing
* Classification using Logistic Regression, Decision Tree, and Random Forest
* Class imbalance analysis using class weighting and SMOTE
* Random Forest hyperparameter tuning using GridSearchCV
* Fare prediction using Linear Regression
* Model evaluation and comparison
* Saving and testing the final machine learning pipeline

## Dataset

The project uses the classic Titanic dataset containing passenger information and survival outcomes.

The dataset was loaded using Seaborn and then saved as `titanic.csv` for reuse in the modeling notebook.

### Data Cleaning

The original dataset contained missing values in `deck`, `age`, `embarked`, and `embark_town`.

The following cleaning steps were applied:

* `deck` was removed because **77.22%** of its values were missing.
* Missing `age` values were filled using the median age.
* Rows with missing `embarked` and `embark_town` values were removed because they represented only **0.22%** of the data.
* An `age_group` feature was created for exploratory analysis.
* After cleaning, the dataset contained **889 rows and 15 columns**.
* The cleaned dataset was saved as `analytics/titanic.csv`.

The cleaning decisions were based on the amount of missing data and the importance of each feature.

## Exploratory Data Analysis (EDA)

The cleaned Titanic dataset contains **889 passengers and 15 columns**. The overall survival rate was approximately **38.25%**.

### Key Findings

* Survival differed substantially by **sex**. The survival rate was approximately **74.04% for females** and **18.89% for males**.
* Survival also differed by **passenger class**. The survival rate was approximately **62.62% in 1st class**, **47.28% in 2nd class**, and **24.24% in 3rd class**.
* The `fare` variable was strongly right-skewed, with a skewness of approximately **4.80**.
* The IQR method identified **65 outliers in age** and **114 outliers in fare**.
* The strongest correlation among the selected numerical variables was between **pclass and fare (-0.5482)**.
* The correlation between **pclass and survival was -0.3355**, showing a moderate negative relationship.

### Visualizations

The EDA includes the following visualizations:

1. Survival rate by **sex and passenger class**
2. **Age distribution** by survival status
3. **Fare vs. age** by survival status
4. Survival rate by **age group and sex**
5. Correlation **heatmap** for selected numerical variables

These visualizations were used to identify patterns in survival and understand how demographic and passenger-related features were associated with the outcome.

## Machine Learning Modeling

The cleaned Titanic dataset was used to build classification models for predicting passenger survival.

### Data Preparation

The data was divided into **80% training data and 20% test data** using a stratified split with `random_state=42`.

Numeric features were processed using:

* Median imputation
* StandardScaler

Categorical features were processed using:

* Most-frequent imputation
* One-hot encoding

The preprocessing steps were included inside a `Pipeline` so that the transformations were learned only from the training data.

### Classification Models

Three classification models were trained using the same train-test split:

* Logistic Regression
* Decision Tree
* Random Forest

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

The initial results were:

| Model               | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| ------------------- | -------: | --------: | -----: | -------: | ------: |
| Logistic Regression |   0.8146 |    0.7966 | 0.6912 |   0.7402 |  0.8678 |
| Decision Tree       |   0.8034 |    0.7463 | 0.7353 |   0.7407 |  0.7850 |
| Random Forest       |   0.7921 |    0.7385 | 0.7059 |   0.7218 |  0.8140 |

Logistic Regression achieved the highest accuracy and ROC-AUC among the initial models.

### Class Imbalance

The target classes were not evenly distributed:

* Not Survived: **61.75%**
* Survived: **38.25%**

To study the effect of class imbalance, Logistic Regression was evaluated using three approaches:

| Approach              | Precision | Recall | F1 Score |
| --------------------- | --------: | -----: | -------: |
| Baseline              |    0.7966 | 0.6912 |   0.7402 |
| Class Weight Balanced |    0.7879 | 0.7647 |   0.7761 |
| SMOTE                 |    0.7812 | 0.7353 |   0.7576 |

Class-weight balancing improved recall and F1 score compared with the baseline model.

### Random Forest Tuning

Random Forest was further tuned using `GridSearchCV` with 5-fold cross-validation.

Best parameters:

* `n_estimators`: **200**
* `max_depth`: **10**
* `max_features`: **sqrt**

The best cross-validation F1 score was **0.7494**, and the OOB score was **0.82**.

## Regression Analysis

A multivariate Linear Regression model was used to predict passenger `fare` using the other available features.

The `fare` column was removed from the input features to avoid target leakage. The same preprocessing approach was used for numeric and categorical features.

### Regression Results

The model was evaluated using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R²
* Adjusted R²

Results:

| Metric      |   Value |
| ----------- | ------: |
| MAE         | 21.2550 |
| RMSE        | 42.4939 |
| R²          |  0.3232 |
| Adjusted R² |  0.2826 |

The model explains approximately **32.32% of the variation in passenger fare**. The residual plot showed that the residual spread increased at higher predicted fare values, indicating **heteroscedasticity**. The visible curved pattern also suggests that the linear model does not fully capture the relationship between the features and fare. A few extreme residuals indicate the presence of outliers.

## Final Model Selection

The final classifier comparison showed the following results:

| Model               | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| ------------------- | -------: | --------: | -----: | -------: | ------: |
| Logistic Regression |   0.8146 |    0.7966 | 0.6912 |   0.7402 |  0.8678 |
| Decision Tree       |   0.8034 |    0.7463 | 0.7353 |   0.7407 |  0.7850 |
| Random Forest       |   0.7921 |    0.7385 | 0.7059 |   0.7218 |  0.8140 |
| Tuned Random Forest |   0.7978 |    0.7667 | 0.6765 |   0.7188 |  0.8154 |

The class-weight-balanced Logistic Regression achieved an F1 score of **0.7761** and recall of **0.7647**, improving performance on the survival class compared with the baseline Logistic Regression.

Based on the evaluation results, the **class-weight-balanced Logistic Regression** was selected as the final classifier because it provided a better balance between precision, recall, and F1 score.

### Model Saving and Testing

The complete preprocessing and classification pipeline was saved using `joblib` as:

`best_titanic_pipeline.joblib`

The saved pipeline was then reloaded and tested using raw passenger feature values. The pipeline successfully generated a prediction, confirming that the trained preprocessing and model steps can be reused after saving.

## How to Run

1. Open the project folder in VS Code or Jupyter Notebook.
2. Install the required Python libraries:

   ```bash
   pip install pandas seaborn matplotlib scikit-learn imbalanced-learn joblib
   ```
3. Open `01_eda.ipynb` and run the cells from top to bottom.
4. The notebook cleans the Titanic dataset and saves the result as `titanic.csv`.
5. Open `02_modeling.ipynb` and run the cells from top to bottom.
6. The modeling notebook trains, evaluates, and compares the classification and regression models.
7. The final classification pipeline is saved as `best_titanic_pipeline.joblib`.

The notebooks should be run in order because the modeling notebook uses the cleaned `titanic.csv` created by the EDA notebook.

### Exploratory Standardization

For exploratory analysis, `age` and `fare` were standardized using `StandardScaler`. After standardization, both variables had means very close to **0** and standard deviations close to **1**. This transformation was used only for exploration and was not used as the final model input because the modeling pipeline performs its own preprocessing.
