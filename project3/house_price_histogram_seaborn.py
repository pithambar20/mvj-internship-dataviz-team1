# Histogram of house prices using Seaborn
# Dataset: Bengaluru_House_Data.xlsx

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the Excel dataset
file_path = "Bengaluru_House_Data.xlsx"
df = pd.read_excel(file_path)

# Convert the price column to numeric and remove missing values
house_prices = pd.to_numeric(df["price"], errors="coerce").dropna()

# Create the histogram
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(
    data=house_prices,
    bins=30,
    kde=True,
    color="skyblue",
    edgecolor="black"
)

# Add chart title and labels
plt.title("Distribution of House Prices in Bengaluru", fontsize=15)
plt.xlabel("House Price (in Lakhs)", fontsize=12)
plt.ylabel("Number of Houses", fontsize=12)
plt.tight_layout()

# Display and save the chart
plt.savefig("house_price_histogram.png", dpi=300)
plt.show()
