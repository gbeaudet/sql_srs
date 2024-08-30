import pandas as pd
import duckdb as dd
import streamlit as st
import io

st.title("""
SQL SRS
Spaced Repetition System SQL practice
""")

# Déclaration des dataframes et des autres variables :
csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = dd.sql(answer).df()


# Sidebar :
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Please select a theme...",
    )
    st.write('You selected the following theme:', option)


# Question SQL par la collègue :
st.header("Enter your code:")
query = st.text_area(label="Your SQL code here:", key="user_input")
if query:
    result = dd.sql(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution)

with tab3:
    st.write(answer)