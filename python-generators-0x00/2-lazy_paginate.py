seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches paginated data from the user_data table
    """
    offset = 0
    while True:  # ✅ One loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ YIELD generator
        offset += page_size
