from sqlite3 import connect, Row, Connection


def connect_database() -> Connection:
    with connect("database/database.sqlite") as conn:
        conn.row_factory = Row
        return conn


def create_table_user():
    conn = connect_database()
    conn.execute(
    """CREATE TABLE IF NOT EXISTS user(
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL,
        password TEXT NOT NULL);"""
    )
    conn.commit()
    conn.close()


def create_table_task():
    conn = connect_database()
    conn.execute(
    """CREATE TABLE IF NOT EXISTS task(
        id_task INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(256) NOT NULL,
        discription TEXT NOT NULL,
        fk_user INTEGER NOT NULL,
        FOREIGN KEY(fk_user) REFERENCES user(id_user) ON DELETE CASCADE);""")
    conn.commit()
    conn.close()

def create_all():
    create_table_user()
    create_table_task()
