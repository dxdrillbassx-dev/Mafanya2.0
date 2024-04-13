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
            print("- [Mafanya] Подключение к базе данных успешно установлено!")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при подключении к базе данных:")
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

                # Создаем таблицу для мутов, если она не существует
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_mutes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        mute_duration INT,
                        mute_count INT DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES user_coins(user_id)
                    )
                """)
            self.conn.commit()
            print("- [Mafanya] Таблицы успешно созданы или уже существуют.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при создании таблиц в базе данных:")
            print(e)

    def add_mute(self, user_id, duration):
        try:
            with self.conn.cursor() as cursor:
                # Проверяем, есть ли уже запись о муте для данного пользователя
                cursor.execute("SELECT * FROM user_mutes WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result:
                    # Если запись уже есть, обновляем ее данные
                    cursor.execute(
                        "UPDATE user_mutes SET mute_duration = %s, mute_count = mute_count + 1 WHERE user_id = %s",
                        (duration, user_id))
                else:
                    # Если записи нет, создаем новую
                    cursor.execute("INSERT INTO user_mutes (user_id, mute_duration) VALUES (%s, %s)",
                                   (user_id, duration))
            self.conn.commit()
            print("- [Mafanya] Информация о муте успешно добавлена в базу данных.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при добавлении информации о муте в базу данных:")
            print(e)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("- [Mafanya] Соединение с базой данных успешно закрыто.")