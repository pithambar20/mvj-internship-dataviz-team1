
# Bengaluru House Price Data - Heat Map
# Libraries required: pandas, openpyxl, matplotlib, seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# STEP 1: LOAD THE EXCEL DATASET
# --------------------------------------------------

file_path = Path("Bengaluru_House_Data.xlsx")

if not file_path.exists():
    raise FileNotFoundError(
        "Excel file not found! Keep Bengaluru_House_Data.xlsx "
        "in the same folder as this Python program."
    )

df = pd.read_excel(file_path)

print("\nDataset loaded successfully!")
print("\nFirst five rows:")
print(df.head())

print("\nDataset columns:")
print(df.columns.tolist())

# --------------------------------------------------
# STEP 2: CLEAN NUMERIC DATA
# --------------------------------------------------

for col in df.columns:
    if df[col].dtype == "object":
        cleaned = df[col].astype(str).str.replace(
            ",", "", regex=False
        )
        converted = pd.to_numeric(cleaned, errors="coerce")

        if converted.notna().sum() >= max(3, len(df) * 0.5):
            df[col] = converted

# --------------------------------------------------
# STEP 3: CREATE CORRELATION HEAT MAP
# --------------------------------------------------

numeric_data = df.select_dtypes(include="number")

if numeric_data.shape[1] >= 2:

    correlation = numeric_data.corr()

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title(
        "Bengaluru House Data - Correlation Heat Map",
        fontsize=14
    )

    plt.tight_layout()

    plt.savefig(
        "house_data_correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("\nCorrelation heat map saved successfully!")

    plt.show()

else:
    print("Not enough numeric columns for correlation heat map.")

# --------------------------------------------------
# STEP 4: FIND LOCATION AND PRICE COLUMNS
# --------------------------------------------------

def find_column(columns, possible_names):
    for col in columns:
        normalized = str(col).strip().lower().replace("_", " ")
        if normalized in possible_names:
            return col
    return None


location_col = find_column(
    df.columns,
    {"location", "area", "locality"}
)

price_col = find_column(
    df.columns,
    {"price", "price lakhs", "price in lakhs"}
)

# --------------------------------------------------
# STEP 5: CREATE LOCATION-WISE PRICE HEAT MAP
# --------------------------------------------------

if location_col is not None and price_col is not None:

    df[price_col] = pd.to_numeric(
        df[price_col].astype(str).str.replace(
            ",", "", regex=False
        ),
        errors="coerce"
    )

    df[location_col] = df[location_col].astype(str).str.strip()

    valid_data = df.dropna(subset=[price_col]).copy()

    valid_data = valid_data[
        (valid_data[location_col] != "") &
        (valid_data[location_col].str.lower() != "nan")
    ]

    average_prices = (
        valid_data.groupby(location_col)[price_col]
        .mean()
        .sort_values(ascending=False)
        .head(20)
    )

    if not average_prices.empty:

        plt.figure(figsize=(9, 8))

        sns.heatmap(
            average_prices.to_frame(name="Average Price"),
            annot=True,
            cmap="YlOrRd",
            fmt=".2f",
            linewidths=0.5,
            cbar_kws={"label": "Average Price"}
        )

        plt.title(
            "Top 20 Bengaluru Locations by Average House Price",
            fontsize=13
        )

        plt.xlabel("Average House Price")
        plt.ylabel("Location")

        plt.tight_layout()

        plt.savefig(
            "location_average_price_heatmap.png",
            dpi=300,
            bbox_inches="tight"
        )

        print("Location-wise price heat map saved successfully!")

        plt.show()

    else:
        print("No valid location and price records found.")

else:
    print(
        "\nLocation or price columns were not found. "
        "Check the column names printed above."
    )

# --------------------------------------------------
# STEP 6: FINISH
# --------------------------------------------------

print("\nProgram completed!")
print("Check the folder for the generated PNG heat maps.")
