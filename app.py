# pylint: disable=(missing-module-docstring)
# pylint: disable-message=F0010
import io

import duckdb as dd
import pandas as pd
import streamlit as st

st.title(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

# Déclaration des dataframes et des autres variables :
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = dd.sql(ANSWER_STR).df()

# Sidebar :
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Please select a theme...",
    )
    st.write("You selected the following theme:", option)

# Question SQL par la collègue :
st.header("Enter your code:")
query = st.text_area(label="Your SQL code here:", key="user_input")
if query:
    result = dd.sql(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing!")

    nb_lines_difference = result.shape[0] - solution_df.shape[0]
    if nb_lines_difference != 0:
        st.write(
            f"Result has a {nb_lines_difference} lines difference with the solution!"
        )

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
