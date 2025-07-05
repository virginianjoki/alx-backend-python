import mysql.connector


def stream_user_ages():
    """
    Generator that yields one user age at a time from the user_data table
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:  # ✅ Loop 1
            yield row[0]

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def average_age():
    """
    Consumes the age stream and calculates the average without using SQL AVG
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ Loop 2
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users in database.")
