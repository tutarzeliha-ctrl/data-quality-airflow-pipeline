import random
from datetime import datetime, timedelta

print("Generating 1 Million rows of synthetic sales data...")

stores = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana"]
customers = [f"C{str(i).zfill(4)}" for i in range(1, 5000)]
products = [f"P{str(i).zfill(3)}" for i in range(501, 550)]

file_path = "data/raw_sales.csv"
start_date = datetime(2025, 1, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write("transaction_id,customer_id,product_id,amount,transaction_date,store_location\n")
    
    for i in range(1, 1000001):
        t_id = 100000 + i
        c_id = random.choice(customers)
        p_id = random.choice(products)
        # Bilinçli olarak bazı boş (null) alanlar bırakıyoruz (Veri kalitesi testi için)
        amount = round(random.uniform(50.0, 5000.0), 2) if random.random() > 0.05 else ""
        days_offset = random.randint(0, 365)
        t_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        store = random.choice(stores)
        
        f.write(f"{t_id},{c_id},{p_id},{amount},{t_date},{store}\n")

print("1 Million rows successfully generated at data/raw_sales.csv! 🚀")