import psycopg2
def create_table():
    cur.execute("""CREATE TABLE userinfo(
                id SERIAL PRIMARY KEY,
                name VARCHAR(15) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(30) NOT NULL UNIQUE
                );
                """)
    cur.execute("""CREATE TABLE mobnumber(
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES userinfo(id),
                number VARCHAR UNIQUE constraint mobnumber_PhoneNumber check (number not like '%[^0-9]%')
                );
                """)
    return conn.commit()

def create_user(cursor, name: str, last_name: str, email: str):
    cursor.execute("""
    INSERT INTO userinfo(name, last_name, email) VALUES (%s, %s, %s);\
    """, (name, last_name, email))
    return conn.commit()

def get_id_user(email: str):
    cur.execute("""
                SELECT id FROM userinfo
                WHERE email= %s;""", (email,))
    user_id = cur.fetchone()
    return user_id[0]

def add_number(cursor, number: int, email: str):
    usersid = get_id_user(email)
    cursor.execute("""
    INSERT INTO mobnumber(user_id, number) VALUES (%s, %s);\
    """, (usersid, number,))
    return conn.commit()

def edite_user(cursor, useremail, name=None, last_name=None, email=None):
    usersid = get_id_user(useremail)
    cursor.execute("""
    UPDATE userinfo SET name=%s, last_name=%s, email=%s WHERE id=%s;\
    """, (name, last_name, email, usersid,))
    return conn.commit()

def delete_number(cursor, email: str):
    usersid = get_id_user(email)
    cursor.execute("""
    DELETE FROM mobnumber WHERE user_id=%s;\
    """, (usersid,))
    return conn.commit()


def delete_user(cursor, email: str):
    usersid = get_id_user(email)
    cursor.execute("""
                DELETE FROM userinfo WHERE id=%s;\
                """, (usersid,))
    return conn.commit()

def search_user(cursor):
    name = input("Введите имя ")
    last_name = input("Введите фамилию ")
    email = input("Введите email ")
    number = input("Введите номер телефона ")
    cur.execute("""
    SELECT name, last_name, email FROM userinfo
    WHERE email=%s OR name=%s OR last_name=%s;
    """, (email, name, last_name))
    cur.execute("""
    SELECT name, last_name, email FROM userinfo u
    JOIN mobnumber m ON m.user_id=u.id
    WHERE m.number=%s;
    """, (number,))
    user_info = cur.fetchall()
    return print("Вот такую информацию получили по вашему запросу ", user_info)

with psycopg2.connect(database='netology_db', user='postgres', password='') as conn:
    with conn.cursor() as cur:
        # create_table()
        # create_user(cur, "Егор", "Самойлов", "pewewer@yahsk.df")
        # add_number(cur, 89643647159, "sobaka@mail.com")
        # edite_user(cur, "Олеган", "Пупкин", "sobak657a@mail.com", "perdun33@yashik.du")
        # delete_number(cur, "sobaka@mail.com")
        # delete_user(cur, "sobaka@mail.com")
        search_user(cur)










