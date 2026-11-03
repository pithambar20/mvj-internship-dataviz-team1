
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------------
# STEP 1: LOAD DATASET
# -----------------------------------------

file_path = Path("Bengaluru_House_Data.xlsx")

if not file_path.exists():
    raise FileNotFoundError(
        "Place Bengaluru_House_Data.xlsx "
        "in the same folder as this Python file."
    )

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")
print("Rows and columns:", df.shape)
print("Available columns:", df.columns.tolist())

# -----------------------------------------
# STEP 2: FIND PRICE COLUMN
# -----------------------------------------

def find_column(possible_names):
    for col in df.columns:
        name = str(col).strip().lower().replace("_", " ")
        if name in possible_names:
            return col
    return None


price_col = find_column(
    {"price", "house price", "house price lakhs"}
)

if price_col is None:
    raise ValueError(
        "Price column not found. Check the printed column names."
    )

df[price_col] = pd.to_numeric(
    df[price_col].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

df = df.dropna(subset=[price_col])
df = df[df[price_col] > 0].copy()

if df.empty:
    raise ValueError("No valid house-price data found.")

# -----------------------------------------
# STEP 3: FIND A REAL TIME COLUMN
# -----------------------------------------

date_col = find_column(
    {"date", "sale date", "listing date", "date listed",
     "transaction date", "year", "sale year", "month"}
)

output_file = "animated_house_price_time_chart.html"

# -----------------------------------------
# OPTION A: REAL DATE/YEAR DATA
# -----------------------------------------

if date_col is not None:

    if str(date_col).strip().lower() in {"year", "sale year"}:
        df["_time"] = pd.to_numeric(df[date_col], errors="coerce")
        df = df.dropna(subset=["_time"])
        df["_time"] = df["_time"].astype(int).astype(str)
    else:
        df["_time"] = pd.to_datetime(
            df[date_col], errors="coerce"
        )
        df = df.dropna(subset=["_time"])
        df["_time"] = df["_time"].dt.strftime("%Y-%m-%d")

    if df.empty:
        raise ValueError("The time column has no valid dates or years.")

    # Aggregate prices for each time period
    time_data = (
        df.groupby("_time", as_index=False)[price_col]
        .mean()
        .sort_values("_time")
    )

    time_data = time_data.rename(
        columns={"_time": "Time", price_col: "Average Price"}
    )

    # Use cumulative observations so the line grows over time
    time_data["Frame"] = range(1, len(time_data) + 1)

    fig = px.line(
        time_data,
        x="Time",
        y="Average Price",
        animation_frame="Frame",
        markers=True,
        title="Animated House Price Trend Over Time",
        labels={
            "Time": "Date / Year",
            "Average Price": "Average House Price (Lakhs)",
            "Frame": "Animation Step"
        }
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    print("Using the dataset's actual time column:", date_col)

# -----------------------------------------
# OPTION B: NO REAL TIME COLUMN
# -----------------------------------------

else:
    print(
        "\nNo date/year column found. "
        "Creating an illustrative animation by listing order."
    )
    print(
        "This does NOT show historical price changes."
    )

    # Sort prices and create batches for animation
    df = df.sort_values(price_col).reset_index(drop=True)

    batch_size = max(1, len(df) // 10)
    df["Step"] = pd.Series(
        df.index // batch_size,
        index=df.index
    ).clip(upper=9) + 1

    # Animate the distribution of prices across batches
    fig = px.scatter(
        df,
        x=df.index,
        y=price_col,
        animation_frame="Step",
        title="Animated Bengaluru House Price Distribution",
        labels={
            "x": "Listing Sequence (not actual time)",
            price_col: "House Price (Lakhs)",
            "Step": "Animation Step"
        },
        hover_data=[price_col]
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

# -----------------------------------------
# STEP 4: ADD ANIMATION CONTROLS
# -----------------------------------------

fig.update_layout(
    updatemenus=[
        {
            "type": "buttons",
            "showactive": False,
            "x": 1.0,
            "y": 1.15,
            "xanchor": "right",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {
                                "duration": 700,
                                "redraw": True
                            },
                            "transition": {"duration": 300},
                            "fromcurrent": True,
                            "mode": "immediate"
                        }
                    ]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ]
        }
    ]
)

# -----------------------------------------
# STEP 5: EXPORT INTERACTIVE HTML
# -----------------------------------------

fig.write_html(
    output_file,
    full_html=True,
    include_plotlyjs=True,
    auto_play=False
)

print("\nAnimated chart created successfully!")
print("HTML file:", output_file)
print("Open the HTML file in Chrome to interact with it.")

# Display chart
fig.show()



