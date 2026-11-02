
# ==========================================
# BENGALURU HOUSE PRICE - BOX PLOT
# ==========================================

# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Connect Excel file to Python
file_path = "Bengaluru_House_Data.xlsx"

df = pd.read_excel(file_path)

# 3. Display dataset
print("First five rows:")
print(df.head())

# 4. Check dataset information
print("\nDataset Information:")
print(df.info())

# 5. Clean required columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')

plot_df = df[['area_type', 'price']].dropna()

# 6. Create Box Plot
plt.figure(figsize=(12, 6))

sns.boxplot(
    data=plot_df,
    x='area_type',
    y='price'
)

# 7. Customize chart
plt.title("Bengaluru House Prices by Area Type", fontsize=16)
plt.xlabel("Area Type", fontsize=12)
plt.ylabel("Price (Lakhs)", fontsize=12)

plt.xticks(rotation=15)
plt.grid(axis='y', alpha=0.3)

# 8. Display chart
plt.tight_layout()
plt.show()

# 9. Save chart
plt.savefig(
    "bengaluru_box_plot.png",
    dpi=300,
    bbox_inches='tight'
)

print("Box plot created successfully!")
