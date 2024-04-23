import pandas as pd
import sqlite3


# Read the XLSX file using pandas
xlsx_file = 'data/test_api.xlsx'
df = pd.read_excel(xlsx_file)

# Connect to a SQLite database
sqlite_file = 'output.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Create a table in the database
table_name = 'data_table'
df.to_sql(table_name, conn, index=False, if_exists='replace')

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"XLSX file '{xlsx_file}' converted to SQLite database '{sqlite_file}' successfully.")

