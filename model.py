import sqlite3
from datetime import datetime, timedelta
db_path = 'orders_0520.db'

# 如果不存在，就會建立
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
       CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_name TEXT,
            cheese_cake INTEGER DEFAULT 0,
            financier_original INTEGER DEFAULT 0,
            financier_choco INTEGER DEFAULT 0,
            financier_tea INTEGER DEFAULT 0,
            pudding INTEGER DEFAULT 0,
            payment_method TEXT,
            pickup_date TEXT,
            pickup_time TEXT,
            pickup_location TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
def insert_order(user_id, user_name, cheese, financier_original, financier_choco, financier_tea, pudding, payment, pickup_date, pickup_time, pickup_location):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    from datetime import datetime, timedelta
    tw_now = datetime.utcnow() + timedelta(hours=8)
    tw_now_str = tw_now.strftime('%Y-%m-%d %H:%M:%S')

    c.execute('''
        INSERT INTO orders (
            user_id, user_name, cheese_cake, financier_original,
            financier_choco, financier_tea, pudding, payment_method,
            pickup_date, pickup_time, pickup_location, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, user_name, cheese, financier_original, financier_choco,
        financier_tea, pudding, payment, pickup_date, pickup_time, pickup_location, tw_now_str
    ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("資料表已初始化")
