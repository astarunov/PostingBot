import asyncio
import asyncpg
import json
from datetime import datetime

async def table_create():
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS post (
                id SERIAL PRIMARY KEY,
                admin_id VARCHAR(255),
                pics_id VARCHAR(255),
                post_text TEXT,
                buttons JSONB,
                post_date TIMESTAMP
            );
        """)
    finally:
        await conn.close()

async def schedule_post_f(a_id, p_id, p_text):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    try:
        row = await conn.fetchrow("""
            INSERT INTO post(admin_id, pics_id, post_text) 
            VALUES ($1, $2, $3)
            RETURNING id;
        """, a_id, p_id, p_text)

        return row['id'] if row else None
    finally:
        await conn.close()

async def schedule_post_s(post_id, p_date):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    try:
        await conn.execute("""
            UPDATE post 
            SET post_date = $1
            WHERE id = $2;
        """, p_date, post_id)
    finally:
        await conn.close()
async def change_date(a_id, id, p_date):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    await conn.execute("""
            UPDATE post 
            SET post_date = $1, admin_id = $2
            WHERE id = $3;
        """, p_date, a_id, id)

    await conn.close()

async def change_text(a_id, id, p_text):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    await conn.execute("""
                UPDATE post 
                SET post_text = $1, admin_id = $2
                WHERE id = $3;
            """, p_text, a_id, id)

    await conn.close()

async def change_buttons(a_id, id, bttns):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    buttons_json = json.dumps(bttns) if isinstance(bttns, list) else bttns
    await conn.execute("""
                UPDATE post 
                SET buttons = $1, admin_id = $2
                WHERE id = $3;
            """, buttons_json, a_id, id)

    await conn.close()
async def cancel_drop(post_id):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    await conn.execute("""
                        DELETE FROM post WHERE id = $1;

                    """, post_id)

    await conn.close()
async def change_pics(a_id, id, p_id):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    await conn.execute("""
                    UPDATE post 
                    SET pics_id = $1, admin_id = $2
                    WHERE id = $3;
                """, p_id, a_id, id)

    await conn.close()


async def main():
    await table_create()



    a_id = 1
    p_id = "123"
    p_text = "Привет, мир!"
    p_date = datetime.strptime('2024-09-29 10:00:00', '%Y-%m-%d %H:%M:%S')
    await schedule_post_s(a_id, p_date)

    """bttns = [
        {"text": "Кнопка 1", "callback_data": "button_1"},
        {"text": "Кнопка 2", "callback_data": "button_2"}
    ]
    p_date = datetime.strptime('2024-09-25 10:00:00', '%Y-%m-%d %H:%M:%S')
    # Пример переноса поста
    a_id = "1"
    p_id = "123"
    p_date = datetime.strptime('2024-09-25 11:00:00', '%Y-%m-%d %H:%M:%S')
    await reschedule_post(a_id, p_id, p_date)"""


# Запуск основного асинхронного процесса
asyncio.run(main())