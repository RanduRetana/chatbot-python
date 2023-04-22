import mysql.connector as mysql


# create connection to database
def create_conn():
    conn = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="chatbot"
    )
    return conn


def save_user_data(idUser, nombre, Email):
    conn = create_conn()
    cursor = conn.cursor()

    query = "INSERT INTO postschatbot (idUser, nombre, Email) VALUES (%s, %s, %s)"
    values = (idUser, nombre, Email)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
