from train import vn

questions = [
    "Show all customers",
    "How many orders are there?",
    "Show the top 5 selling products",
    "What are the total sales?",
    "Who are the top 5 customers by spending?",
    "Show all products and their prices",
    "Find the total quantity of products sold",
    "Show the number of orders for each customer",
    "Find the average product price",
    "Show the 10 most recent orders"
]

for i, question in enumerate(questions, start=1):

    print("\n" + "=" * 60)
    print(f"TEST {i}: {question}")

    sql = vn.generate_sql(question=question)

    print("\nGenerated SQL:")
    print(sql)

    print("\nCheck SQL manually before execution.")