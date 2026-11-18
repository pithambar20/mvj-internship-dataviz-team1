# Tools I Want to Learn Next: Plotly and Streamlit

Today I spent about 30 minutes learning the basics of Plotly and Streamlit. I am still a beginner, but I understand what each tool is used for and how they can work together in a data visualization project.

## 1. What I learned about Plotly

Plotly is a Python library for making interactive charts. A user can hover over data points to see details, zoom in, and click items in the legend to show or hide categories.

Plotly can create scatter plots, bar charts, line charts and many other chart types. For example, a scatter plot can help compare house size and price across different Bengaluru localities.

### Plotly example: Bengaluru house prices

The following code uses made-up sample values for practice. They are not actual market prices.

```python
import pandas as pd
import plotly.express as px

data = {
    "Locality": [
        "Whitefield", "Whitefield",
        "Electronic City", "Electronic City",
        "Indiranagar", "Indiranagar"
    ],
    "House_Size": [1000, 1500, 900, 1400, 1000, 1600],
    "Price_Lakhs": [55, 88, 35, 62, 90, 155]
}

df = pd.DataFrame(data)

fig = px.scatter(
    df,
    x="House_Size",
    y="Price_Lakhs",
    color="Locality",
    title="Bengaluru House Prices",
    labels={
        "House_Size": "House Size (sq. ft.)",
        "Price_Lakhs": "Price (₹ lakhs)"
    }
)

fig.show()

# Save the interactive chart as an HTML file
fig.write_html("bengaluru_house_prices.html")
```

This code creates a scatter plot with house size on the x-axis and price on the y-axis. Different colours represent different localities. The last line saves the interactive chart as an HTML file that can be opened in a web browser.

To run this in Google Colab, install the required libraries first:

```python
%pip install -q pandas plotly
```

## 2. What I learned about Streamlit

Streamlit is a Python tool for turning a Python script into a small web app. It can display text, tables and charts, and it provides controls such as dropdown menus and sliders so users can explore data.

Plotly and Streamlit have different roles: Plotly makes the interactive chart, while Streamlit creates the app page around it. They can be used together.

### Streamlit example: House-price explorer

Save this code in a file named `app.py`.

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bengaluru House Price Explorer")
st.write("Explore a small sample of house sizes and prices.")

data = {
    "Locality": [
        "Whitefield", "Whitefield",
        "Electronic City", "Electronic City",
        "Indiranagar", "Indiranagar"
    ],
    "House_Size": [1000, 1500, 900, 1400, 1000, 1600],
    "Price_Lakhs": [55, 88, 35, 62, 90, 155]
}

df = pd.DataFrame(data)

locality = st.selectbox(
    "Choose a locality",
    ["All"] + sorted(df["Locality"].unique().tolist())
)

if locality != "All":
    df = df[df["Locality"] == locality]

st.dataframe(df)

fig = px.scatter(
    df,
    x="House_Size",
    y="Price_Lakhs",
    color="Locality",
    title="House Size vs Price",
    labels={
        "House_Size": "House Size (sq. ft.)",
        "Price_Lakhs": "Price (₹ lakhs)"
    }
)

st.plotly_chart(fig, use_container_width=True)
```

Install the libraries and run the app from a terminal on your computer:

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

Streamlit opens the app in a browser. The dropdown lets the user choose a locality, and the table and chart update to show the selected data.

## 3. What I understood after the introduction

- **Plotly** is mainly for creating interactive charts.
- **Streamlit** is for building simple web apps with Python.
- They can be combined so a Streamlit app displays Plotly charts.
- Plotly charts can be exported as HTML and opened in a browser.

In this short introduction, I focused on understanding the basic purpose of each tool and trying a small example. My next step is to run the Plotly code, explore the chart by hovering and zooming, and then try the Streamlit app.

*Note: All house-price values in these examples are invented for practice only. They should not be treated as real Bengaluru property prices.*
