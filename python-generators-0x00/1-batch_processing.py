import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user rows from the database
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch  # ✅ yield generator used
                batch = []

        if batch:
            yield batch  # ✅ yield the final batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter and print users older than 25
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ 1st loop
        for user in batch:  # ✅ 2nd loop
            if user["age"] > 25:
                print(user)
