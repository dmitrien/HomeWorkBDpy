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
    pass


def create_user(cursor, name: str, last_name: str, email: str):
    cursor.execute("""
    INSERT INTO userinfo(name, last_name, email) VALUES (%s, %s, %s);\
    """, (name, last_name, email))
    pass


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
    pass


def edite_user(cursor, useremail, name=None, last_name=None, email=None):
    usersid = get_id_user(useremail)
    if name!=None:
        cursor.execute("""
        UPDATE userinfo SET name=%s WHERE id=%s;\
        """, (name, usersid,))
    if last_name!=None:
        cursor.execute("""
        UPDATE userinfo SET last_name=%s WHERE id=%s;\
        """, (last_name, usersid,))
    if email!=None:
        cursor.execute("""
        UPDATE userinfo SET email=%s WHERE id=%s;\
        """, (email, usersid,))
    pass


def delete_number(cursor, email: str):
    usersid = get_id_user(email)
    cursor.execute("""
    DELETE FROM mobnumber WHERE user_id=%s;\
    """, (usersid,))
    pass


def delete_user(cursor, email: str):
    usersid = get_id_user(email)
    delete_number(cursor, email)
    cursor.execute("""
                DELETE FROM userinfo WHERE id=%s;\
                """, (usersid,))
    pass


def search_user(cursor, name=None, last_name=None, email=None, number=None):
    if name!=None:
        cursor.execute("""
            SELECT name, last_name, email FROM userinfo
            WHERE name=%s;
            """, (name,))
    if last_name!=None:
        cursor.execute("""
            SELECT name, last_name, email FROM userinfo
            WHERE last_name=%s;
            """, (last_name,))
    if email!=None:
        cursor.execute("""
            SELECT name, last_name, email FROM userinfo
            WHERE email=%s;
            """, (email,))
    if number!=None:
        cursor.execute("""
        SELECT name, last_name, email FROM userinfo u
        JOIN mobnumber m ON m.user_id=u.id
        WHERE m.number=%s;
        """, (number,))
    user_info = cur.fetchall()
    return print("Вот такую информацию получили по вашему запросу ", user_info)


if __name__ == '__main__':
    with psycopg2.connect(database='netology_db', user='postgres', password='') as conn:
        with conn.cursor() as cur:
            # create_table()
            # create_user(cur, "Петр", "Примеров", "pew5ew45er@ya7sk.df")
            # add_number(cur, 89645647199, "pewewer@yahsk.df")
            # edite_user(cur, "pewewer@yahsk.df", "Пупкинec", "Тестович")
            # delete_number(cur, "sobaka@mail.com")
            # delete_user(cur, "pewewer@yahsk.df")
            # search_user(cur, 'Петр',)
    conn.close()
