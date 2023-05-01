import mysql.connector as mysql


# create connection to database
def create_conn():
    conn = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="hunterprice"
    )
    return conn


def save_user_data(user_id, meta_key, meta_value):
    conn = create_conn()
    cursor = conn.cursor()

    query = "INSERT INTO ewsjujoc_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)"
    values = (user_id, meta_key, meta_value)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
