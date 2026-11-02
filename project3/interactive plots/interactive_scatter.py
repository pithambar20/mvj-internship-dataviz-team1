
# 1. Import libraries
import pandas as pd
import plotly.express as px

# 2. Connect Excel file
df = pd.read_excel("Bengaluru_House_Data.xlsx")

# 3. Convert columns to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

df['total_sqft'] = pd.to_numeric(
    df['total_sqft'].astype(str).str.replace(",", ""),
    errors='coerce'
)

# 4. Remove missing values
plot_df = df.dropna(
    subset=['total_sqft', 'price', 'area_type']
)

# 5. Create interactive scatter plot
fig = px.scatter(
    plot_df,
    x='total_sqft',
    y='price',
    color='area_type',
    hover_name='location',
    hover_data=['size', 'bath', 'balcony'],
    title='Bengaluru House Prices vs Total Square Feet',
    labels={
        'total_sqft': 'Total Area (Square Feet)',
        'price': 'Price (Lakhs)',
        'area_type': 'Area Type'
    },
    opacity=0.75
)

# 6. Customize chart
fig.update_traces(marker=dict(size=9))

fig.update_layout(
    title_x=0.5,
    template='plotly_white',
    xaxis_title='Total Area (Square Feet)',
    yaxis_title='Price (Lakhs)'
)

# 7. Display chart
fig.show()

# 8. Export to HTML
fig.write_html('bengaluru_interactive_scatter.html')

print("Interactive scatter plot created successfully!")
