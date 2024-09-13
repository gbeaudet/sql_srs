# pylint: disable=(missing-module-docstring)
# pylint: disable-message=F0010

import ast

import duckdb
import streamlit as st

st.title(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution_df = dd.sql(ANSWER_STR).df()

# Sidebar :
with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Please select a theme...",
    )
    st.write("You selected the following theme:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

# Requête SQL de l'utilisateur :
st.header("Enter your code:")
query = st.text_area(label="Your SQL code here:", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

#    try:
#        result = result[solution_df.columns]
#        st.dataframe(result.compare(solution_df))
#    except KeyError as e:
#        st.write("Some columns are missing!")

#    #nb_lines_difference = result.shape[0] - solution_df.shape[0]
#    if nb_lines_difference != 0:
#        st.write(
#            f"Result has a {nb_lines_difference} lines difference with the solution!"
#        )

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    st.write(answer)
