from tortoise import Tortoise
from data.config import MySQL
from loguru import logger

connection_string = f'mysql://{MySQL.user}:{MySQL.password}@{MySQL.host}:{MySQL.port}/{MySQL.database}'
modules = {'models': ['database.models']}

async def load_database(*_, **__):
    await Tortoise.init(db_url=connection_string, modules=modules)
    await Tortoise.generate_schemas()
    logger.info('Database loaded')
