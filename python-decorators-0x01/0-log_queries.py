import sqlite3
import functools

#  Decorator to log SQL queries


def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from positional or keyword arguments
        query = None
        if args:
            query = args[0]  # assuming the first argument is always the query
        elif 'query' in kwargs:
            query = kwargs['query']

        print(f"[LOG] Executing SQL Query: {query}")
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


#  Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
