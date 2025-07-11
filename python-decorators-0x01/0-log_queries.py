import sqlite3
import functools
from datetime import datetime

#  Decorator to log SQL queries with timestamps


def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from positional or keyword arguments
        query = None
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']

        # Log query with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL Query: {query}")
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#  Test the logging with timestamp
users = fetch_all_users(query="SELECT * FROM users")
print(users)
