
# 1. Import libraries
import pandas as pd
import plotly.express as px

# 2. Connect Excel file
df = pd.read_excel("Bengaluru_House_Data.xlsx")

# 3. Convert price to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 4. Remove missing values
plot_df = df[['area_type', 'price']].dropna()

# 5. Create interactive violin plot
fig = px.violin(
    plot_df,
    x='area_type',
    y='price',
    color='area_type',
    box=True,
    points='outliers',
    title='Bengaluru House Prices by Area Type',
    labels={
        'area_type': 'Area Type',
        'price': 'Price (Lakhs)'
    }
)

# 6. Customize chart
fig.update_layout(
    title_x=0.5,
    xaxis_title='Area Type',
    yaxis_title='Price (Lakhs)',
    showlegend=False,
    template='plotly_white'
)

# 7. Display interactive chart
fig.show()

# 8. Export to HTML
fig.write_html('bengaluru_interactive_violin_plot.html')

print("Interactive violin plot created successfully!")
