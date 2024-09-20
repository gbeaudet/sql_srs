# pylint: disable=(missing-module-docstring)
# pylint: disable-message=F0010

import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
test = con.execute("SELECT * FROM memory_state").df()
print(test)
