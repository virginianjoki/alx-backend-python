import time
import sqlite3
import functools

#  Shared query cache
query_cache = {}

#  with_db_connection from previous tasks


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

#  cache_query decorator


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract SQL query from args or kwargs
        query = None
        if args:
            # assume query is first positional argument after conn
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']

        # Check cache
        if query in query_cache:
            print("[CACHE HIT] Returning cached result for query.")
            return query_cache[query]

        print("[CACHE MISS] Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#  First call will run the query and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#  Second call will use cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
