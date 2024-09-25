import asyncio
import asyncpg
import json
from datetime import datetime

async def table_create():
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
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
    await conn.close()


async def schedule_post(a_id, p_id, p_text, bttns, p_date):
    conn = await asyncpg.connect(user='postgres', password='qwe123rtz456', database='postgres', host='localhost')
    buttons_json = json.dumps(bttns) if isinstance(bttns, list) else bttns

    await conn.execute("""
        INSERT INTO post(admin_id, pics_id, post_text, buttons, post_date) 
        VALUES ($1, $2, $3, $4, $5);
    """, a_id, p_id, p_text, buttons_json, p_date)

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
    """a_id = "1"
    p_id = "123"
    p_text = "Привет, мир!"
    bttns = [
        {"text": "Кнопка 1", "callback_data": "button_1"},
        {"text": "Кнопка 2", "callback_data": "button_2"}
    ]
    p_date = datetime.strptime('2024-09-25 10:00:00', '%Y-%m-%d %H:%M:%S')
    await schedule_post(a_id, p_id, p_text, bttns, p_date)
    a_id = "2"
    p_id = "123"
    p_date = datetime.strptime('2024-09-25 11:00:00', '%Y-%m-%d %H:%M:%S')
    await change_date(a_id, p_id, p_date)
    a_id = "3"
    p_id = "123"
    p_text = "Пока"
    await change_text(a_id, p_id, p_text)
    a_id = "1"
    id = 1
    bttns = [
        {"text": "Кнопка 3", "callback_data": "button_1"},
        {"text": "Кнопка 4", "callback_data": "button_2"}
    ]
    await change_buttons(a_id, id, bttns)"""
    a_id = "1234"
    id = 1
    p_id = "12332, 123312"
    await change_pics(a_id, id, p_id)
asyncio.run(main())
