
# ==========================================
# BENGALURU HOUSE PRICE - VIOLIN PLOT
# ==========================================

# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 2. Read the Excel file in the same folder as this script
data_file = Path(__file__).resolve().with_name("Bengaluru_House_Data.xlsx")
df = pd.read_excel(data_file)

# 4. Display dataset
print("First five rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

# 5. Clean the required columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')

plot_df = df[['area_type', 'price']].dropna()

# 6. Create Violin Plot
plt.figure(figsize=(12, 6))

sns.violinplot(
    data=plot_df,
    x='area_type',
    y='price',
    inner='quartile',
    cut=0
)

# 7. Add chart labels
plt.title(
    'Bengaluru House Prices by Area Type',
    fontsize=16
)

plt.xlabel('Area Type', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)

plt.xticks(rotation=15)
plt.grid(axis='y', alpha=0.3)

# 8. Save and display chart
plt.tight_layout()
output_file = Path(__file__).resolve().with_name('bengaluru_violin_plot.png')
plt.savefig(
    output_file,
    dpi=300,
    bbox_inches='tight'
)

plt.show()
