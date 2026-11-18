
# 1. Import libraries
import pandas as pd
import plotly.express as px

# 2. Read Excel file
df = pd.read_excel("Bengaluru_House_Data.xlsx")

# 3. Select numerical columns
numeric_df = df.select_dtypes(include="number")

# 4. Calculate correlation
correlation = numeric_df.corr()

# 5. Create interactive heatmap
fig = px.imshow(
    correlation,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Bengaluru House Data - Correlation Heatmap",
    labels={
        "x": "Features",
        "y": "Features",
        "color": "Correlation"
    }
)

# 6. Customize chart
fig.update_layout(
    width=900,
    height=700,
    title_x=0.5
)

# 7. Display interactive chart
fig.show()

# 8. Export to HTML
fig.write_html("bengaluru_interactive_heatmap.html")

print("Interactive heatmap created successfully!")
