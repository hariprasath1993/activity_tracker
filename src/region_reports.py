import streamlit as st
import pandas as pd
import plotly.express as px
from utils.utils import Utils

st.header("Lead Classification")

# Fetch accounts
accounts = Utils.fetch_all_accounts()

# Extract categories
categories = []
for account in accounts:
    category = account['properties']['Category']['select']
    if category:
        categories.append(category['name'])
    else:
        categories.append('Uncategorised')

# Create a DataFrame
df = pd.DataFrame(categories, columns=['Category'])

# Count the occurrences of each category
category_counts = df['Category'].value_counts().sort_index().reset_index()
category_counts.columns = ['Category', 'Count']

# Create an interactive bar chart using Plotly
fig = px.bar(category_counts, x='Category', y='Count',
             title='Account Category Distribution',
             labels={'Category': 'Category', 'Count': 'Count'},
             text='Count', color='Category')

# Update layout to rotate x-axis labels for better readability
fig.update_layout(xaxis_tickangle=-45)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)
