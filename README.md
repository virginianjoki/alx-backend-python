# Python Generators — Task 0: Database Setup

This script sets up a MySQL database `ALX_prodev` with a `user_data` table, and populates it with rows from `user_data.csv`.

### Functions

- `connect_db()`: Connects to MySQL server
- `create_database(connection)`: Creates `ALX_prodev` if not exists
- `connect_to_prodev()`: Connects to the ALX_prodev database
- `create_table(connection)`: Creates the `user_data` table
- `insert_data(connection, csv_file)`: Populates table from CSV file

> Ensure MySQL is running and credentials are correct before executing.
