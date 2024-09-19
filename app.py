# pylint: disable=(missing-module-docstring)
# pylint: disable-message=F0010
import io

<<<<<<< HEAD
import io
import logging
import os

import duckdb
=======
import duckdb as dd
import pandas as pd
>>>>>>> df2e180be6348d152022375e7d449600a14e1283
import streamlit as st

st.title(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

<<<<<<< HEAD
# Vérification existence répertoire data/ (céation si besoin) :
if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

# Vérification existence fichier exercices_sql_tables.duckdb (création si besoin) :
if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())  # pylint disable!
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
=======
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
>>>>>>> df2e180be6348d152022375e7d449600a14e1283

# Sidebar :
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Please select a theme...",
    )
<<<<<<< HEAD
    st.write("You selected the following theme:", theme)

    # On va trier par ancienneté, et on reset l'index :
    exercise = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)

    try:
        exercise_name = exercise.loc[0, "exercise_name"]
    except KeyError as e:
        st.write("No theme selected!")

    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

# Requête SQL de l'utilisateur :
=======
    st.write("You selected the following theme:", option)

# Question SQL par la collègue :
>>>>>>> df2e180be6348d152022375e7d449600a14e1283
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
<<<<<<< HEAD
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)

=======
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
>>>>>>> df2e180be6348d152022375e7d449600a14e1283
