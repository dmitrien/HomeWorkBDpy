import psycopg2

with psycopg2.connect(database='netology_db', user='postgres', password='1507') as conn:
    with conn.cursor() as cur:
        def create_table():
            cur.execute("""CREATE TABLE userinfo(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(15) NOT NULL,
                        second_name VARCHAR(30) NOT NULL,
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
        # create_table()

        def create_user(cursor, name: str, second_name: str, email: str):
            cursor.execute("""
            INSERT INTO userinfo(name, second_name, email) VALUES (%s, %s, %s);\
            """, (name, second_name, email))
            return conn.commit()


        # create_user(cur, "Егор", "Самойлов", "pewewer@yahsk.df")

        def get_id_user( email: str):
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

        # add_number(cur, 89643647159, "sobaka@mail.com")

        def edite_user(cursor, name: str, second_name: str, email: str, useremail: str):
            usersid = get_id_user(useremail)
            cursor.execute("""
            UPDATE userinfo SET name=%s, second_name=%s, email=%s WHERE id=%s;\
            """, (name, second_name, email, usersid,))
            return conn.commit()

        # edite_user(cur, "Олеган", "Пупкин", "sobak657a@mail.com", "perdun33@yashik.du")

        def delete_number(cursor, email: str):
            usersid = get_id_user(email)
            cursor.execute("""
            DELETE FROM mobnumber WHERE user_id=%s;\
            """, (usersid,))
            return conn.commit()

        # delete_number(cur, "sobaka@mail.com")

        def delete_user(cursor, email: str):
            usersid = get_id_user(email)
            cursor.execute("""
                        DELETE FROM userinfo WHERE id=%s;\
                        """, (usersid,))
            return conn.commit()
        # delete_user(cur, "sobaka@mail.com")

        def search_user(cursor):
            name = input("Введите имя ")
            second_name = input("Введите фамилию ")
            email = input("Введите email ")
            number = input("Введите номер телефона ")
            cur.execute("""
            SELECT name, second_name, email FROM userinfo
            WHERE email=%s OR name=%s OR second_name=%s;
            """, (email, name, second_name))
            cur.execute("""
            SELECT name, second_name, email FROM userinfo u
            JOIN mobnumber m ON m.user_id=u.id
            WHERE m.number=%s;
            """, (number,))
            user_info = cur.fetchall()
            return print("Вот такую информацию получили по вашему запросу ", user_info)

        # search_user(cur)










