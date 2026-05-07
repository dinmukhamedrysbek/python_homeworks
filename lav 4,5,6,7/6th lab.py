import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

# 1. Load data
df = pd.read_excel("catalog_products.xlsx")

print("Shape:", df.shape)
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nFirst 5 rows:")
print(df.head())

# 2. Convert numeric columns to float and fill missing values
numeric_cols = ['col_2','col_3','col_4','col_5','col_6','col_8','col_9','col_10','col_11']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].mean())

print("\nMissing values after cleaning:")
print(df[numeric_cols].isnull().sum())

# 3. New columns
df['total_value'] = df['col_2'] * df['col_3']
df['double_stock'] = df['col_4'] * 2
df['log_price'] = np.log(df['col_2'])

# 4. Expensive electronics
electronics_expensive = df[(df['col_2'] > 500) & (df['col_7'] == "Electronics")]
print("\nExpensive Electronics:")
print(electronics_expensive.head())

# 5. Group by category
category_stats = df.groupby('col_7').agg(
    mean_price=('col_2', 'mean'),
    max_price=('col_2', 'max'),
    total_quantity=('col_3', 'sum')
).reset_index()

print("\nCategory Stats:")
print(category_stats.head())

# 6. Summary statistics
summary = pd.DataFrame({
    'column': numeric_cols,
    'mean': [df[c].mean() for c in numeric_cols],
    'median': [df[c].median() for c in numeric_cols],
    'std': [df[c].std() for c in numeric_cols]
})

print("\nSummary statistics:")
print(summary)

# 7. Price anomalies
mean_price = df['col_2'].mean()
std_price = df['col_2'].std()

anomalies = df[df['col_2'] > mean_price + 3 * std_price]

print("\nPrice anomalies:")
print(anomalies.head())

# 8. Correlation matrix
corr_matrix = df[numeric_cols].corr()

print("\nCorrelation matrix:")
print(corr_matrix)

# 9. Histogram of price
plt.figure(figsize=(10,6))
plt.hist(df['col_2'], bins=50)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.grid(True)
plt.show()

# 10. Price vs quantity
plt.figure(figsize=(10,6))
sns.regplot(x='col_2', y='col_3', data=df)
plt.title("Price vs Quantity")
plt.xlabel("Price")
plt.ylabel("Quantity")
plt.show()

# 11. Price by category
plt.figure(figsize=(12,6))
sns.boxplot(x='col_7', y='col_2', data=df)
plt.title("Price by Category")
plt.xlabel("Category")
plt.ylabel("Price")
plt.xticks(rotation=45)
plt.show()

# 12. Pairplot
sns.pairplot(df[['col_2','col_3','col_4','col_5','col_6','col_7']], hue='col_7')
plt.show()

# 13. Heatmap correlation
plt.figure(figsize=(12,8))
sns.heatmap(corr_matrix, annot=True)
plt.title("Correlation Heatmap")
plt.show()

# 14. Save processed data
df.to_excel("catalog_analysis.xlsx", index=False)

# 15. Final category summary
category_summary = df.groupby('col_7').agg(
    count=('col_1', 'count'),
    mean_price=('col_2', 'mean'),
    total_quantity=('col_3', 'sum'),
    mean_log_price=('log_price', 'mean')
).reset_index()

print("\nCategory Summary:")
print(category_summary.head())

# 16. Most expensive product in each category
idx = df.groupby('col_7')['col_2'].idxmax()

most_expensive = df.loc[idx, ['col_1', 'col_2', 'col_7']]

print("\nMost expensive products:")
print(most_expensive)

# 17. Top 10 by total value
top10_value = df.sort_values('total_value', ascending=False).head(10)

print("\nTop 10 by total value:")
print(top10_value[['col_1','col_2','col_3','total_value']])

# 18. Price ranges
bins = [0, 50, 200, 500, 1000, np.inf]
labels = ['0-50', '50-200', '200-500', '500-1000', '>1000']

df['price_range'] = pd.cut(df['col_2'], bins=bins, labels=labels)

price_range_count = df['price_range'].value_counts().reset_index()
price_range_count.columns = ['price_range', 'count']

print("\nPrice ranges:")
print(price_range_count)

plt.figure(figsize=(8,5))
sns.barplot(x='price_range', y='count', data=price_range_count)
plt.title("Number of Products by Price Range")
plt.xlabel("Price Range")
plt.ylabel("Count")
plt.show()

# 19. Total stock value by category
category_stock_value = df.groupby('col_7')['total_value'].sum().reset_index()
category_stock_value.columns = ['category', 'total_stock_value']

print("\nCategory with max stock value:")
print(category_stock_value.sort_values('total_stock_value', ascending=False).head(1))

plt.figure(figsize=(10,6))
sns.barplot(x='category', y='total_stock_value', data=category_stock_value)
plt.title("Total Stock Value by Category")
plt.xlabel("Category")
plt.ylabel("Total Stock Value")
plt.xticks(rotation=45)
plt.show()

# 20 / 36. Mean price and mean quantity by category
category_mean = df.groupby('col_7').agg(
    mean_price=('col_2', 'mean'),
    mean_quantity=('col_3', 'mean')
).reset_index()

print("\nMean price and quantity by category:")
print(category_mean)

plt.figure(figsize=(10,6))
sns.scatterplot(x='mean_price', y='mean_quantity', hue='col_7', data=category_mean)
plt.title("Mean Price and Mean Quantity by Category")
plt.xlabel("Mean Price")
plt.ylabel("Mean Quantity")
plt.show()

# 21 / 37. Price standard deviation by category
std_price_category = df.groupby('col_7')['col_2'].std().reset_index()
std_price_category.columns = ['category', 'std_price']

print("\nPrice std by category:")
print(std_price_category)

plt.figure(figsize=(10,6))
sns.barplot(x='std_price', y='category', data=std_price_category)
plt.title("Price Standard Deviation by Category")
plt.xlabel("Standard Deviation of Price")
plt.ylabel("Category")
plt.show()

# 22 / 38. Products with zero stock
zero_stock = df[df['col_3'] == 0][['col_1','col_7','col_2']]

print("\nZero stock products:")
print(zero_stock.head(10))

# 23 / 39. Top 5 categories by count
top5_categories = df['col_7'].value_counts().head(5).reset_index()
top5_categories.columns = ['category', 'count']

print("\nTop 5 categories:")
print(top5_categories)

plt.figure(figsize=(10,6))
sns.barplot(x='category', y='count', data=top5_categories)
plt.title("Top 5 Categories by Number of Products")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

# 24 / 40. Top 10 by stock
top_stock = df.sort_values('col_3', ascending=False).head(10)

print("\nTop 10 by stock:")
print(top_stock[['col_1','col_3']])

plt.figure(figsize=(10,6))
sns.barplot(x='col_3', y='col_1', data=top_stock)
plt.title("Top 10 Products by Stock")
plt.xlabel("Quantity")
plt.ylabel("Product")
plt.show()

# 25 / 41. Heatmap category and price range
pivot = pd.pivot_table(
    df,
    index='col_7',
    columns='price_range',
    values='col_1',
    aggfunc='count',
    fill_value=0
)

print("\nPivot table:")
print(pivot)

plt.figure(figsize=(10,6))
sns.heatmap(pivot, annot=True, fmt='d')
plt.title("Products by Category and Price Range")
plt.xlabel("Price Range")
plt.ylabel("Category")
plt.show()

# 42. Price vs rating
plt.figure(figsize=(10,6))
sns.regplot(x='col_2', y='col_5', data=df)
plt.title("Price vs Rating")
plt.xlabel("Price")
plt.ylabel("Rating")
plt.show()

# 43. Pairplot again
sns.pairplot(df[['col_2','col_3','col_4','col_5','col_6','col_7']], hue='col_7')
plt.show()

# 44. Extreme items by price or stock
price_limit = df['col_2'].mean() + 3 * df['col_2'].std()
stock_limit = df['col_3'].mean() + 3 * df['col_3'].std()

extreme_items = df[
    (df['col_2'] > price_limit) |
    (df['col_3'] > stock_limit)
]

print("\nExtreme items:")
print(extreme_items.head())

# 45. Final Excel report
with pd.ExcelWriter("catalog_final_report.xlsx") as writer:
    df.to_excel(writer, sheet_name="Processed Data", index=False)
    category_summary.to_excel(writer, sheet_name="Category Summary", index=False)
    top_stock.to_excel(writer, sheet_name="Top Stock", index=False)
    top10_value.to_excel(writer, sheet_name="Top Value", index=False)
    category_stock_value.to_excel(writer, sheet_name="Stock Value", index=False)
    most_expensive.to_excel(writer, sheet_name="Most Expensive", index=False)

print("\nDone! Files saved:")
print("catalog_analysis.xlsx")
print("catalog_final_report.xlsx")