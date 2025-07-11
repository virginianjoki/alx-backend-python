import sqlite3

#  Custom context manager for executing queries


class ExecuteQuery:
    def __init__(self, query, params=()):
        self.db_name = 'users.db'
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # Return result directly in `with` block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("[INFO] Connection closed after query.")


#  Use the reusable query context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
