import streamlit as st
import pandas as pd
import duckdb as dd


# 08/08/2024 : Tests divers :
#st.write("Hello world")
#input_text = st.text_area(label='Enter your input')
#st.write(input_text)


# 08/08/2024 : Test avec un df et des requêtes SQL :
st.title("SQL")
st.write("Dataframe :")
data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
df = pd.DataFrame(data)
st.dataframe(df)

## Essai (réussi) :
#sql_query = st.text_area('Enter your SQL request')
#st.write(dd.query(sql_query))

## Correction :
# On crée notre zone de texte où l'utilisateur va taper sa requête SQL :
sql_query = st.text_area('Enter your SQL request')

# On récupère la requête SQL brute qu'on exécute via duckdb, et qu'on convertie en df :
result = dd.query(sql_query).df()

# On affiche la requête tapée par l'utilisateur :
st.write(f'Vous avez entré la query suivante : {sql_query}')

# On affiche le résultat sous forme de df :
st.dataframe(result)
