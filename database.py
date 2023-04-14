import mysql.connector as mysql


# create connection to database
def create_conn():
    conn = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="chatbotpython"
    )
    return conn


def save_user_data(name, email):
    conn = create_conn()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
