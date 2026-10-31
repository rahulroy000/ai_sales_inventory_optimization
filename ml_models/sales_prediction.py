
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# STEP 1: Make output folder
folder = "outputs/ml_models"
os.makedirs(folder, exist_ok=True)

# STEP 2: Style settings
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 3: Load data
df = pd.read_csv("data/processed/cleaned_data.csv")

# STEP 4: Prepare data types
numeric_columns = [
    "quantity_sold",
    "discount_pct",
    "current_stock",
    "lead_time_days"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# STEP 5: Select features and target
features = [
    "category",
    "discount_pct",
    "current_stock",
    "lead_time_days"
]

target = "quantity_sold"

df = df.dropna(subset=[target])

X = df[features]
y = df[target]

print("\nFEATURE INFORMATION")
print(X.info())

print("\nTARGET INFORMATION")
print(y.describe())

# STEP 6: Identify numerical and categorical columns
categorical_features = ["category"]

numerical_features = [
    "discount_pct",
    "current_stock",
    "lead_time_days"
]

# STEP 7: Preprocessing
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# STEP 8: Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTRAINING ROWS:", len(X_train))
print("TESTING ROWS:", len(X_test))

# STEP 9: Create Linear Regression Model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)

# STEP 10: Train model
model.fit(X_train, y_train)

print("\nMODEL TRAINING COMPLETED")

# STEP 11: Prediction
y_pred = model.predict(X_test)

# STEP 12: Model Performance
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print("\nLINEAR REGRESSION PERFORMANCE")

print("MAE  :", round(mae, 2))
print("MSE  :", round(mse, 2))
print("RMSE :", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# STEP 13: Actual vs Predicted Table
result = pd.DataFrame({
    "Actual Quantity": y_test.values,
    "Predicted Quantity": y_pred.round(2)
})

print("\nACTUAL VS PREDICTED SALES")
print(result.head(15).to_string(index=False))

result.to_csv(
    f"{folder}/sales_prediction_results.csv",
    index=False
)

# STEP 14: Actual vs Predicted Graph
plt.figure(figsize=(10, 7))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.6
)

minimum = min(y_test.min(), y_pred.min())
maximum = max(y_test.max(), y_pred.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--",
    linewidth=2
)

plt.title(
    "Actual vs Predicted Sales Quantity",
    fontsize=18
)

plt.xlabel("Actual Quantity Sold", fontsize=13)
plt.ylabel("Predicted Quantity Sold", fontsize=13)

plt.tight_layout()

plt.savefig(
    f"{folder}/sales_prediction_graph.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# STEP 15: Take User Input
print("\nENTER PRODUCT DETAILS FOR SALES PREDICTION")

category = input("Enter Product Category: ")

discount = float(input("Enter Discount: "))

current_stock = float(input("Enter Current Stock: "))

lead_time_days = float(input("Enter Lead Time Days: "))

user_data = pd.DataFrame([{
    "category": category,
    "discount_pct": discount,
    "current_stock": current_stock,
    "lead_time_days": lead_time_days
}])

# STEP 16: Predict Sales Quantity
prediction = model.predict(user_data)

print("\nPREDICTED SALES QUANTITY:",
      max(0, round(prediction[0])))
