
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------
# STEP 1: LOAD EXCEL DATA
# -----------------------------------

file_path = Path("Bengaluru_House_Data.xlsx")

if not file_path.exists():
    raise FileNotFoundError(
        "Excel file not found. Keep it in the same folder "
        "as this Python program."
    )

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
print("Available columns:", df.columns.tolist())

# -----------------------------------
# STEP 2: SELECT HOUSE PRICE COLUMN
# -----------------------------------

price_column = next(
    (
        col for col in df.columns
        if str(col).strip().lower() in
        ["price", "house_price", "house price"]
    ),
    None
)

if price_column is None:
    raise ValueError(
        "Price column not found. Check the column names printed above."
    )

# Convert price values to numbers
df[price_column] = pd.to_numeric(
    df[price_column].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

# Remove missing and invalid values
df = df.dropna(subset=[price_column])
df = df[df[price_column] > 0]

if df.empty:
    raise ValueError("No valid house-price values found.")

# -----------------------------------
# STEP 3: CREATE INTERACTIVE HISTOGRAM
# -----------------------------------

fig = px.histogram(
    df,
    x=price_column,
    nbins=30,
    title="Interactive Histogram of Bengaluru House Prices",
    labels={
        price_column: "House Price (Lakhs)",
        "count": "Number of Houses"
    },
    color_discrete_sequence=["royalblue"],
    hover_data=[price_column]
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="House Price (Lakhs)",
    yaxis_title="Number of Houses",
    bargap=0.08
)

fig.update_traces(
    hovertemplate=(
        "Price range: %{x}<br>"
        "Number of houses: %{y}"
        "<extra></extra>"
    )
)

# -----------------------------------
# STEP 4: EXPORT TO HTML
# -----------------------------------

output_file = "interactive_house_price_histogram.html"

fig.write_html(
    output_file,
    include_plotlyjs=True,
    full_html=True
)

print("\nInteractive histogram created successfully!")
print("HTML file:", output_file)
print("Valid house-price records:", len(df))

# Display the interactive chart
fig.show()
