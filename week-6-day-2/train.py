import os
from pathlib import Path
from dotenv import load_dotenv

from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

load_dotenv(Path(__file__).parent / ".env")


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):

    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


vn = MyVanna(config={
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-4o-mini"
})

# Connect MySQL
vn.connect_to_mysql(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", "3306"))
)

# Train using 5 examples
training_data = [
    (
        "Show all customers",
        "SELECT * FROM customers;"
    ),
    (
        "Find total number of orders",
        "SELECT COUNT(*) AS total_orders FROM orders;"
    ),
    (
        "Find top 5 selling products",
        """
        SELECT p.product_name,
               SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
        LIMIT 5;
        """
    ),
    (
        "Calculate total sales",
        """
        SELECT SUM(quantity * price) AS total_sales
        FROM order_items;
        """
    ),
    (
        "Find top 5 customers by spending",
        """
        SELECT c.customer_name,
               SUM(oi.quantity * oi.price) AS total_spending
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spending DESC
        LIMIT 5;
        """
    )
]

for question, sql in training_data:
    vn.train(question=question, sql=sql)
    print("Trained:", question)

print("\nVanna training completed successfully!")
