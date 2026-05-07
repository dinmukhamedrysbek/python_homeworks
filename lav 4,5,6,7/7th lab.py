# MACHINE LEARNING PROJECT
# Product Price Prediction

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, confusion_matrix

sns.set()

# =========================
# Task 1. Load and explore data
# =========================

df = pd.read_excel("catalog_products.xlsx")

print("First 5 rows:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nUseful columns for price prediction:")
print("Useful columns can be stock, rating, sales, discount, category, and other numeric product characteristics.")
print("Target column is col_2 because it represents price.")

# =========================
# Task 2. Cleaning data
# =========================

target = "col_2"
category_col = "col_7"
product_name_col = "col_1"

# Try to convert all possible numeric columns to float
for col in df.columns:
    if col not in [product_name_col, category_col]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill numeric missing values with mean
numeric_cols = df.select_dtypes(include=[np.number]).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

# Drop rows with missing text values
df = df.dropna(subset=[product_name_col, category_col])

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# =========================
# Task 3. Create new features
# =========================

df["total_value"] = df["col_2"] * df["col_3"]
df["log_price"] = np.log(df["col_2"])
df["double_stock"] = df["col_3"] * 2

print("\nNew features:")
print(df[["total_value", "log_price", "double_stock"]].head())

# =========================
# Task 4. Visual analysis
# =========================

plt.figure(figsize=(10, 6))
plt.hist(df["col_2"], bins=50)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x="col_2", y="col_3", data=df)
plt.title("Price vs Stock Quantity")
plt.xlabel("Price")
plt.ylabel("Quantity")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="col_7", y="col_2", data=df)
plt.title("Price by Category")
plt.xlabel("Category")
plt.ylabel("Price")
plt.xticks(rotation=45)
plt.show()

# =========================
# Task 5. Detect and remove anomalies
# =========================

price_mean = df["col_2"].mean()
price_std = df["col_2"].std()

lower_limit = price_mean - 3 * price_std
upper_limit = price_mean + 3 * price_std

anomalies = df[
    (df["col_2"] > upper_limit) |
    (df["col_2"] < lower_limit)
]

print("\nAnomalies:")
print(anomalies.head())

df_clean = df[
    (df["col_2"] <= upper_limit) &
    (df["col_2"] >= lower_limit)
].copy()

print("\nShape after removing anomalies:")
print(df_clean.shape)

# =========================
# Task 6. Encode categorical features
# =========================

df_encoded = pd.get_dummies(df_clean, columns=["col_7"], drop_first=True)

# Remove product name because it is text
df_encoded = df_encoded.drop(columns=["col_1"])

print("\nData types after encoding:")
print(df_encoded.dtypes)

# =========================
# Task 7. Split X and y
# =========================

y = df_encoded["col_2"]

# Basic model features
X_basic = df_encoded.drop(columns=["col_2", "total_value", "log_price"])

X_train, X_test, y_train, y_test = train_test_split(
    X_basic,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTrain shape:", X_train.shape)
print("Test shape:", X_test.shape)

# =========================
# Task 8. Simple Linear Regression
# =========================

lr_basic = LinearRegression()
lr_basic.fit(X_train, y_train)

y_pred_basic = lr_basic.predict(X_test)

mae_basic = mean_absolute_error(y_test, y_pred_basic)
mse_basic = mean_squared_error(y_test, y_pred_basic)

print("\nBasic Linear Regression:")
print("MAE:", mae_basic)
print("MSE:", mse_basic)

# =========================
# Task 9. Improved Linear Regression
# =========================
# Note: total_value and log_price are based on price.
# In real ML this is data leakage, but we include them because the task asks.

X_improved = df_encoded.drop(columns=["col_2"])

X_train_imp, X_test_imp, y_train_imp, y_test_imp = train_test_split(
    X_improved,
    y,
    test_size=0.2,
    random_state=42
)

lr_improved = LinearRegression()
lr_improved.fit(X_train_imp, y_train_imp)

y_pred_improved = lr_improved.predict(X_test_imp)

mae_improved = mean_absolute_error(y_test_imp, y_pred_improved)
mse_improved = mean_squared_error(y_test_imp, y_pred_improved)

print("\nImproved Linear Regression:")
print("MAE:", mae_improved)
print("MSE:", mse_improved)

# =========================
# Task 10. Visualization of predictions
# =========================

plt.figure(figsize=(8, 6))
plt.scatter(y_test_imp, y_pred_improved, alpha=0.5)
plt.plot([y_test_imp.min(), y_test_imp.max()],
         [y_test_imp.min(), y_test_imp.max()])
plt.title("True Price vs Predicted Price")
plt.xlabel("True Price")
plt.ylabel("Predicted Price")
plt.grid(True)
plt.show()

errors = pd.DataFrame({
    "true_price": y_test_imp,
    "predicted_price": y_pred_improved,
    "error": abs(y_test_imp - y_pred_improved)
})

print("\nWorst predictions:")
print(errors.sort_values("error", ascending=False).head())

# =========================
# Task 11. Normalization
# =========================

scale_cols = ["col_3", "col_4", "total_value", "double_stock", "log_price"]

scaler = StandardScaler()

scaled_data = scaler.fit_transform(df_clean[scale_cols])

scaled_df = pd.DataFrame(
    scaled_data,
    columns=[col + "_scaled" for col in scale_cols]
)

print("\nScaled features mean:")
print(scaled_df.mean())

# =========================
# Task 12. Feature Importance
# =========================

tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(X_train_imp, y_train_imp)

importance_df = pd.DataFrame({
    "feature": X_improved.columns,
    "importance": tree_reg.feature_importances_
}).sort_values("importance", ascending=False)

print("\nFeature importance:")
print(importance_df.head(10))

plt.figure(figsize=(10, 6))
sns.barplot(x="importance", y="feature", data=importance_df.head(10))
plt.title("Top 10 Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

y_pred_tree = tree_reg.predict(X_test_imp)

mae_tree = mean_absolute_error(y_test_imp, y_pred_tree)
mse_tree = mean_squared_error(y_test_imp, y_pred_tree)

print("\nDecision Tree Regressor:")
print("MAE:", mae_tree)
print("MSE:", mse_tree)

# =========================
# Task 13. Polynomial Features
# =========================

poly_cols = ["col_3", "col_4", "col_5", "col_6", "double_stock"]

X_poly_base = df_clean[poly_cols]
y_poly = df_clean["col_2"]

X_train_poly, X_test_poly, y_train_poly, y_test_poly = train_test_split(
    X_poly_base,
    y_poly,
    test_size=0.2,
    random_state=42
)

poly = PolynomialFeatures(degree=2, include_bias=False)

X_train_poly_new = poly.fit_transform(X_train_poly)
X_test_poly_new = poly.transform(X_test_poly)

poly_model = LinearRegression()
poly_model.fit(X_train_poly_new, y_train_poly)

y_pred_poly = poly_model.predict(X_test_poly_new)

mae_poly = mean_absolute_error(y_test_poly, y_pred_poly)
mse_poly = mean_squared_error(y_test_poly, y_pred_poly)

print("\nPolynomial Linear Regression:")
print("MAE:", mae_poly)
print("MSE:", mse_poly)

# =========================
# Task 14. KNN Regressor
# =========================

X_knn = X_basic
y_knn = y

X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
    X_knn,
    y_knn,
    test_size=0.2,
    random_state=42
)

knn_scaler = StandardScaler()

X_train_knn_scaled = knn_scaler.fit_transform(X_train_knn)
X_test_knn_scaled = knn_scaler.transform(X_test_knn)

knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_knn_scaled, y_train_knn)

y_pred_knn = knn.predict(X_test_knn_scaled)

mae_knn = mean_absolute_error(y_test_knn, y_pred_knn)
mse_knn = mean_squared_error(y_test_knn, y_pred_knn)

print("\nKNN Regressor:")
print("MAE:", mae_knn)
print("MSE:", mse_knn)

# =========================
# Model comparison
# =========================

model_results = pd.DataFrame({
    "model": [
        "Basic Linear Regression",
        "Improved Linear Regression",
        "Decision Tree",
        "Polynomial Regression",
        "KNN"
    ],
    "MAE": [
        mae_basic,
        mae_improved,
        mae_tree,
        mae_poly,
        mae_knn
    ],
    "MSE": [
        mse_basic,
        mse_improved,
        mse_tree,
        mse_poly,
        mse_knn
    ]
})

print("\nModel comparison:")
print(model_results)

# =========================
# Task 15. Separate models by category
# =========================

category_results = []

for category in df_clean["col_7"].unique():
    category_data = df_clean[df_clean["col_7"] == category].copy()

    if len(category_data) > 20:
        X_cat = category_data.select_dtypes(include=[np.number]).drop(
            columns=["col_2", "total_value", "log_price"]
        )
        y_cat = category_data["col_2"]

        X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
            X_cat,
            y_cat,
            test_size=0.2,
            random_state=42
        )

        model_cat = LinearRegression()
        model_cat.fit(X_train_cat, y_train_cat)

        y_pred_cat = model_cat.predict(X_test_cat)

        mae_cat = mean_absolute_error(y_test_cat, y_pred_cat)

        category_results.append({
            "category": category,
            "MAE": mae_cat
        })

category_results_df = pd.DataFrame(category_results)

print("\nMAE by category:")
print(category_results_df)

# =========================
# Task 16. Prediction visualization by category
# =========================

for category in df_clean["col_7"].unique():
    category_data = df_clean[df_clean["col_7"] == category].copy()

    if len(category_data) > 20:
        X_cat = category_data.select_dtypes(include=[np.number]).drop(
            columns=["col_2", "total_value", "log_price"]
        )
        y_cat = category_data["col_2"]

        X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
            X_cat,
            y_cat,
            test_size=0.2,
            random_state=42
        )

        model_cat = LinearRegression()
        model_cat.fit(X_train_cat, y_train_cat)

        y_pred_cat = model_cat.predict(X_test_cat)

        plt.figure(figsize=(6, 5))
        plt.scatter(y_test_cat, y_pred_cat, alpha=0.5)
        plt.plot([y_test_cat.min(), y_test_cat.max()],
                 [y_test_cat.min(), y_test_cat.max()])
        plt.title(f"True vs Predicted Price: {category}")
        plt.xlabel("True Price")
        plt.ylabel("Predicted Price")
        plt.grid(True)
        plt.show()

# =========================
# Task 17. Cross-validation
# =========================

cv_model = DecisionTreeRegressor(random_state=42)

mae_scores = cross_val_score(
    cv_model,
    X_improved,
    y,
    cv=5,
    scoring="neg_mean_absolute_error"
)

mse_scores = cross_val_score(
    cv_model,
    X_improved,
    y,
    cv=5,
    scoring="neg_mean_squared_error"
)

print("\nCross-validation Decision Tree:")
print("Mean MAE:", -mae_scores.mean())
print("Mean MSE:", -mse_scores.mean())

# =========================
# Task 18. Price classification
# =========================

def price_class(price):
    if price < 100:
        return 0
    elif price <= 500:
        return 1
    else:
        return 2

df_clean["price_class"] = df_clean["col_2"].apply(price_class)

df_class = pd.get_dummies(df_clean, columns=["col_7"], drop_first=True)
df_class = df_class.drop(columns=["col_1"])

X_class = df_class.drop(
    columns=["col_2", "total_value", "log_price", "price_class"]
)
y_class = df_class["price_class"]

X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(
    X_class,
    y_class,
    test_size=0.2,
    random_state=42
)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train_class, y_train_class)

y_pred_class = clf.predict(X_test_class)

accuracy = accuracy_score(y_test_class, y_pred_class)

print("\nDecision Tree Classifier:")
print("Accuracy:", accuracy)

# =========================
# Task 19. Confusion Matrix
# =========================

cm = confusion_matrix(y_test_class, y_pred_class)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Low", "Medium", "High"],
    yticklabels=["Low", "Medium", "High"]
)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.show()

print("\nConfusion matrix:")
print(cm)

# =========================
# Task 20. Save final predictions
# =========================

final_data = df_clean.copy()

# Predict prices for all data using improved regression model
final_encoded = pd.get_dummies(final_data, columns=["col_7"], drop_first=True)
final_encoded = final_encoded.drop(columns=["col_1"])

# Align columns with training data
final_X = final_encoded.drop(columns=["col_2"])
final_X = final_X.reindex(columns=X_improved.columns, fill_value=0)

final_data["predicted_price"] = lr_improved.predict(final_X)

# Predict classes
final_class_encoded = pd.get_dummies(final_data, columns=["col_7"], drop_first=True)
final_class_encoded = final_class_encoded.drop(columns=["col_1", "predicted_price"])

final_X_class = final_class_encoded.drop(
    columns=["col_2", "total_value", "log_price", "price_class"]
)
final_X_class = final_X_class.reindex(columns=X_class.columns, fill_value=0)

final_data["predicted_class"] = clf.predict(final_X_class)

final_data.to_excel("catalog_ml_predictions.xlsx", index=False)

print("\nFinal file saved:")
print("catalog_ml_predictions.xlsx")

# =========================
# Final visual report
# =========================

plt.figure(figsize=(8, 6))
plt.scatter(y_test_imp, y_pred_improved, alpha=0.5)
plt.plot([y_test_imp.min(), y_test_imp.max()],
         [y_test_imp.min(), y_test_imp.max()])
plt.title("Final Report: True vs Predicted Price")
plt.xlabel("True Price")
plt.ylabel("Predicted Price")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x="importance", y="feature", data=importance_df.head(10))
plt.title("Final Report: Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Low", "Medium", "High"],
    yticklabels=["Low", "Medium", "High"]
)
plt.title("Final Report: Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.show()