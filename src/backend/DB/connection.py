
import aiomysql
import logging

from aiomysql import Connection
from src.backend.config import HOST, USER, PASSWORD, DATABASE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

db_config = {
  'host': HOST,
  'user': USER,
  'password': PASSWORD,
  'db': DATABASE,
  'port': 3306
}

async def create_connection() -> Connection:
  try:
      connection = await aiomysql.connect(**db_config)
      if connection:
          logger.info(
              f"Успешное подключение к MySQL серверу (версия {connection.get_server_info()})")
          return connection
      else:
          print(f"Ошибка подключения к MySQL серверу")
  except Exception as e:
      print(f"Ошибка при выполнении запроса: {e}")