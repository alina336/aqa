import allure
import psycopg2
from utils.logging_config import logger
from psycopg2.extras import RealDictCursor


class DBClient:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    @allure.step("Подключение к базе данных")
    def create_connection(self):
        try:
            logger.info("Подключение к БД")
            connection = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user,
                                          password=self.password)
            return connection
        except psycopg2.Error as e:
            logger.error(f"Ошибка создания подключения к БД: {e}")
            raise

    @allure.step("Создание курсора")
    def create_cursor(self, connection):
        try:
            logger.info("Создание курсора")
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            return cursor
        except psycopg2.Error as e:
            logger.error(f"Ошибка создания курсора: {e}")
            raise

    @allure.step("Закрытие соединения")
    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            try:
                logger.info("Закрытие соединения")
                self.connection.close()
            except psycopg2.Error as e:
                logger.error(f"Ошибка при закрытии соединения: {e}")

    def close_cursor(self):
        logger.info("Закрытие курсора")
        self.cursor.close()

    def execute(self, query, params=None):
        logger.info(f"Отправлен запрос в БД: {query}")
        try:
            with allure.step(f"Выполнение запроса {query}"):
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                if query.strip().upper().startswith('SELECT'):
                    result = self.cursor.fetchall()
                    dict_result = [dict(row) for row in result]
                    logger.info(f"Результат запроса: {dict_result}")
                    return dict_result
                else:
                    self.connection.commit()
                    return None
        except psycopg2.Error as e:
            logger.error(f"Ошибка выполнения запроса: {e}")

    def __enter__(self):
        self.connection = self.create_connection()
        self.cursor = self.create_cursor(self.connection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_cursor()
        self.close_connection()

    # def insert_into_table(self, table_name, data):
    #     columns = ",".join(data.keys())
    #     values = ",".join([f"'{value}'" for value in data.values()])
    #     query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    #     self.execute(query)


    # def insert_pet_data(self, mapped_data):
    #     self.insert_into_table("pets", mapped_data["pets"])
    #     self.insert_into_table("categories", mapped_data["categories"])
    #     for tag in mapped_data["tags"]:
    #         self.insert_into_table("tags", tag)
    #     for photo in mapped_data["photos"]:
    #         self.insert_into_table("photos", photo)
