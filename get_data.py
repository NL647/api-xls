import sqlite3

def get_data_by_hostname(hostname):
    sqlite_file = 'output.db'  # Replace with your SQLite database file

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Execute the query to fetch data
    c.execute(f"SELECT * FROM data_table WHERE LOWER(Hostname) = LOWER(?)", (hostname,))
    rows = c.fetchall()
    print (hostname)

    # Execute the query to fetch column names
    c.execute(f"PRAGMA table_info(data_table)")
    columns = [column[1] for column in c.fetchall()]

    # Close the connection
    conn.close()

    print(rows)
    print(columns)

    return columns, rows


#recherche par application + wildcard (like)
def get_data_by_application(application):
    sqlite_file = 'output.db'  # Replace with your SQLite database file

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Execute the query to fetch data
    c.execute(f"SELECT * FROM data_table WHERE LOWER(Application) LIKE LOWER(?)", (f"{application}%",))
    rows = c.fetchall()

    # Execute the query to fetch column names
    c.execute(f"PRAGMA table_info(data_table)")
    columns = [column[1] for column in c.fetchall()]

    # Close the connection
    conn.close()

    return columns, rows


   