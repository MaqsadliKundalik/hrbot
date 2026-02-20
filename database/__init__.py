from tortoise import Tortoise
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['database.models']},
    )
    await Tortoise.generate_schemas()

#     await migrate_db()

# async def migrate_db():
#     conn = Tortoise.get_connection("default")
#     tables = ["teacher_resumes", "admins_resumes", "tg_users"]
#     for table in tables:
#         try:
#             await conn.execute_query(
#                 f"ALTER TABLE {table} ALTER COLUMN created_at "
#                 f"TYPE TIMESTAMPTZ USING created_at AT TIME ZONE 'UTC'"
#             )
#         except Exception as e:
#             print(f"migrate_db [{table}]: {e}")


    
async def close_db():
    await Tortoise.close_connections()
