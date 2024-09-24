import psycopg2

conn = psycopg2.connect(host = "localhost", dbname = "postgres", user = "postgres", password = "qwe123rtz456", port = 5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);
""")

conn.commit()
cur.close()
conn.close()