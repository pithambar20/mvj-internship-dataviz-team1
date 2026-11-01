# What I Learned About Plotly and Streamlit

## 1. Plotly

-   Plotly is a Python library used to create interactive charts and
    graphs.
-   It supports bar charts, line charts, scatter plots and many other
    visualizations.
-   We can hover over a chart to see values and zoom in to explore the
    data.
-   Plotly Express makes it easier to create charts with less code.

### Example: Creating a Bar Chart

``` python
import plotly.express as px

data = {
    "Fruit": ["Apple", "Banana", "Mango"],
    "Quantity": [10, 15, 8]
}

fig = px.bar(data, x="Fruit", y="Quantity", title="Fruit Quantity")
fig.show()
```

This code creates an interactive bar chart showing the quantity of each
fruit.

## 2. Streamlit

-   Streamlit is a Python framework used to turn Python scripts into web
    applications.
-   It provides simple commands to add headings, text, input fields,
    tables and charts.
-   It is useful for creating dashboards and displaying data analysis
    results.
-   We can run an application using the `streamlit run app.py` command.

### Example: Creating a Simple Streamlit App

Save this code in a file named `app.py`.

``` python
import streamlit as st

st.title("My First Data App")
st.write("Learning Streamlit")

name = st.text_input("Enter your name")

if name:
    st.write("Hello,", name)

st.bar_chart({
    "Sales": [100, 150, 120, 200]
})
```

Run the application using:

``` bash
pip install streamlit
streamlit run app.py
```

This creates a simple web app with a text input and a sales chart.

## 3. What I Understood

Plotly is mainly used to create interactive visualizations, while
Streamlit is used to build an application around data and
visualizations. Plotly charts can also be displayed inside a Streamlit
application, which makes it possible to create interactive data
dashboards using Python.
