# pylint: disable=(missing-module-docstring, exec-used, consider-using-with)
# pylint: disable-message=F0010

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
    exec(open("init_db.py", "r", encoding="utf-8").read())  # pylint disable!
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1 : checking the columns
    2 : checking the values
    :param user_query: a string containing the query inserted by the user
    :return:
    """
    result = con.execute(user_query).df()
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


# Sidebar n'affichant que les thèmes existants :
with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    # st.write(available_themes_df["theme"].unique())
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Please select a theme...",
    )

    # Si thème sélectionné, affichage, sinon affichage du dernier thème utilisé :
    if theme:
        st.write(f"You selected the theme {theme}")
        SELECT_EXERCISE_QUERY = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        SELECT_EXERCISE_QUERY = "SELECT * FROM memory_state"

    exercise = (
        con.execute(SELECT_EXERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

# Requête SQL de l'utilisateur :
st.header("Enter your code:")
query = st.text_area(label="Your SQL code here:", key="user_input")

if query:
    check_users_solution(query)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)

# PR du 20/09 am
