import pymysql
import disnake
from disnake.ext import commands


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host="185.112.101.143",
                user="mafanya",
                password="wl_geb/y8CH49bhS",
                database="mafanya",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
            print("- [Mafanya] Подключение к базе данных успешно установлено!")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при подключении к базе данных:")
            print(e)

    # СОЗДАНИЕ ТАБЛИЦ
    def create_tables(self):
        try:
            with self.conn.cursor() as cursor:
                # Создаем таблицу user_coins, если она не существует
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_coins (
                        user_id BIGINT PRIMARY KEY,
                        coins INT NOT NULL DEFAULT 0
                    )
                """
                )

                # Создаем таблицу user_tokens, если она не существует
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_tokens (
                        user_id BIGINT PRIMARY KEY,
                        tokens INT NOT NULL DEFAULT 0
                    )
                """
                )

                # Создаем таблицу для мутов, если она не существует
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_mutes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        mute_duration INT,
                        mute_count INT DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES user_coins(user_id)
                    )
                """
                )

                # Создаем таблицу для активности, если она не существует
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_activity (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        activity_date DATE,
                        activity_type VARCHAR(255),
                        FOREIGN KEY (user_id) REFERENCES user_coins(user_id)
                    )
                """
                )

                # Создаем таблицу для хранения предупреждений
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_warnings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        warn_count INT NOT NULL DEFAULT 0,
                        last_warn_date DATETIME,
                        FOREIGN KEY (user_id) REFERENCES user_coins(user_id)
                    )
                """
                )

                # Создаем таблицу для хранения репутации пользователей
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_reputation (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        giver_id BIGINT NOT NULL,
                        receiver_id BIGINT NOT NULL,
                        date_given DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE INDEX idx_giver_receiver (giver_id, receiver_id)
                        ADD COLUMN reputation INT NOT NULL DEFAULT 0;
                    )
                """
                )
            self.conn.commit()
            print("- [Mafanya] Таблицы успешно созданы или уже существуют.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при создании таблиц в базе данных:")
            print(e)

    # МУТЫ
    def add_mute(self, user_id, duration):
        try:
            with self.conn.cursor() as cursor:
                # Проверяем, есть ли уже запись о муте для данного пользователя
                cursor.execute(
                    "SELECT * FROM user_mutes WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    # Если запись уже есть, обновляем ее данные
                    cursor.execute(
                        "UPDATE user_mutes SET mute_duration = %s, mute_count = mute_count + 1 WHERE user_id = %s",
                        (duration, user_id),
                    )
                else:
                    # Если записи нет, создаем новую
                    cursor.execute(
                        "INSERT INTO user_mutes (user_id, mute_duration) VALUES (%s, %s)",
                        (user_id, duration),
                    )
            self.conn.commit()
            print("- [Mafanya] Информация о муте успешно добавлена в базу данных.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при добавлении информации о муте в базу данных:")
            print(e)

    # ПРЕДУПРЕЖДЕНИЯ
    def add_warning(self, user_id):
        try:
            with self.conn.cursor() as cursor:
                # Проверяем, есть ли уже запись о предупреждениях для данного пользователя
                cursor.execute(
                    "SELECT * FROM user_warnings WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    # Если запись уже есть, обновляем ее данные
                    warn_count = result["warn_count"] + 1
                    cursor.execute(
                        "UPDATE user_warnings SET warn_count = %s, last_warn_date = NOW() WHERE user_id = %s",
                        (warn_count, user_id),
                    )
                else:
                    # Если записи нет, создаем новую
                    cursor.execute(
                        "INSERT INTO user_warnings (user_id, warn_count, last_warn_date) VALUES (%s, 1, NOW())",
                        (user_id,),
                    )
            self.conn.commit()
            print("- [Mafanya] Предупреждение успешно добавлено в базу данных.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при добавлении предупреждения в базу данных:")
            print(e)

    def check_warnings(self, user_id):
        try:
            with self.conn.cursor() as cursor:
                # Проверяем количество предупреждений для данного пользователя
                cursor.execute(
                    "SELECT warn_count FROM user_warnings WHERE user_id = %s",
                    (user_id,),
                )
                result = cursor.fetchone()
                if result:
                    warn_count = result["warn_count"]
                    if warn_count >= 5:
                        # Если количество предупреждений достигло 5, выполняем бан пользователя
                        print(
                            f"Бан пользователя с ID {user_id} из-за 5 предупреждений."
                        )
                        # Ваш код для выполнения бана пользователя
                    elif warn_count >= 3:
                        # Если количество предупреждений достигло 3, выполняем мут пользователя на день
                        print(
                            f"Мут пользователя с ID {user_id} на день из-за 3 предупреждений."
                        )
                        # Ваш код для выполнения мута пользователя на день
                else:
                    print(f"Пользователь с ID {user_id} не имеет предупреждений.")
        except pymysql.Error as e:
            print("- [Mafanya] Ошибка при проверке предупреждений в базе данных:")
            print(e)

    # РЕПУТАЦИЯ
    def check_reputation(self, giver_id, receiver_id):
        if self.conn is None:
            self.connect()  # убедимся, что соединение установлено
        query = "SELECT COUNT(*) as count FROM user_reputation WHERE giver_id = %s AND receiver_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (giver_id, receiver_id))
            result = cursor.fetchone()
            return result['count'] > 0

    def update_reputation(self, receiver_id, points):
        if self.conn is None:
            self.connect()  # Убедимся, что соединение установлено
        query = "UPDATE user_reputation SET reputation = reputation + %s WHERE receiver_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (points, receiver_id))
            self.conn.commit()

    def record_reputation_giving(self, giver_id, receiver_id):
        if self.conn is None:
            self.connect()  # убедимся, что соединение установлено
        query = "INSERT INTO user_reputation (giver_id, receiver_id) VALUES (%s, %s)"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (giver_id, receiver_id))
            self.conn.commit()

    # ЗАКРЫТИЕ СОЕДИНЕНИЯ
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("- [Mafanya] Соединение с базой данных успешно закрыто.")
