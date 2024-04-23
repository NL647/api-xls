import os
import time
from datetime import datetime

def get_database_creation_date():
    sqlite_file = '/home/admin/api-xl/output.db'  # Replace with your SQLite database file path
    timestamp = os.path.getctime(sqlite_file)
    print(timestamp)
    creation_date = datetime.fromtimestamp(timestamp)
    print(creation_date)
    return creation_date


get_database_creation_date()
