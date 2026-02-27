from tortoise import Tortoise
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['database.models']},
    )
    await Tortoise.generate_schemas()

    await migrate_db()

async def migrate_db():
    conn = Tortoise.get_connection("default")
    conn.execute_query("ALTER TABLE tg_users DROP COLUMN IF EXISTS source_of_income")
    
async def close_db():
    await Tortoise.close_connections()
