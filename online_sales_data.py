import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
""")

sample_data = [
    ("Apples", 10, 1.2),
    ("Bananas", 15, 0.5),
    ("Oranges", 8, 0.8),
    ("Apples", 5, 1.2),
    ("Bananas", 20, 0.5),
    ("Grapes", 12, 1.5)
]

cursor.execute("DELETE FROM sales")
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

query = """
    SELECT product, 
        SUM(quantity) AS total_qty, 
        ROUND(SUM(quantity * price), 2) AS revenue
    FROM sales
    GROUP BY product
"""

df = pd.read_sql_query(query, conn)
print("📦 Sales Summary:\n", df)

df.plot(kind='bar', x='product', y='revenue', legend=False, color='orange')
plt.title("💰 Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

conn.close()
