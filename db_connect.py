import pymysql

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host='185.112.101.143',
                user='mafanya',
                password='wl_geb/y8CH49bhS',
                database='mafanya',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Подключение к базе данных успешно установлено!")
        except pymysql.Error as e:
            print("Ошибка при подключении к базе данных:")
            print(e)

    def create_tables(self):
        try:
            with self.conn.cursor() as cursor:
                # Создаем таблицу user_coins, если она не существует
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_coins (
                        user_id BIGINT PRIMARY KEY,
                        coins INT NOT NULL DEFAULT 0
                    )
                """)

                # Создаем таблицу user_tokens, если она не существует
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_tokens (
                        user_id BIGINT PRIMARY KEY,
                        tokens INT NOT NULL DEFAULT 0
                    )
                """)
            self.conn.commit()
            print("Таблицы успешно созданы или уже существуют.")
        except pymysql.Error as e:
            print("Ошибка при создании таблиц в базе данных:")
            print(e)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение с базой данных успешно закрыто.")
