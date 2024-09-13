# pylint: disable=(missing-module-docstring)
# pylint: disable-message=F0010

import io
import logging
import os

import duckdb
import streamlit as st

st.title(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

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

# Sidebar :
with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Please select a theme...",
    )
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
st.header("Enter your code:")
query = st.text_area(label="Your SQL code here:", key="user_input")
if query:
    result = con.execute(query).df()
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)

