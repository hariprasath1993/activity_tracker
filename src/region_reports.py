import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import Utils

st.header("Lead Classification")

accounts = Utils.fetch_all_accounts()
categories = []
for account in accounts:
    category = account['properties']['Category']['select']
    if category:
        categories.append(category['name'])
    else:
        categories.append('Uncategorised')

df = pd.DataFrame(categories, columns=['Category'])

category_counts = df['Category'].value_counts().sort_index()


fig, ax = plt.subplots(figsize=(10, 6))
category_counts.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Account Category Distribution')
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_xticklabels(category_counts.index, rotation=45, ha='right')

# Display the plot in Streamlit
st.pyplot(fig)
