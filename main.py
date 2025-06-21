from faker import Faker
from confluent_kafka import SerializingProducer
import random
from datetime import datetime
import time

fake = Faker()

def generate_sales_transactions():
    user = fake.simple_profile()

    return {
        "transaction_id": fake.uuid4(),
        "process_id": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "product_name": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        "product_category": random.choice(['electronics', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        "product_price" : round(random.uniform(10,1000),2),
        "product_quantity": random.randint(1, 10),
        "product_brand": random.choice(['Apple', 'Samsung', 'mi', 'dell', 'sony']),
        "currency": random.choice(['USD', 'GBP']),
        "customer_id": user['username'],
        "transcation_date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "payment_method": random.choice(['Credit card', 'Debit Card', 'Online transfer'])

    }

def main():
    topic = 'financial_transactions'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9002'
    })

    current_time = datetime.now()
    while (datetime.now() - current_time).total_seconds() < 120:
        try:
            transaction = generate_sales_transactions()
            transaction['total_amount'] = transaction['product_price'] * transaction['product_quantity']

            print(transaction)
            time.sleep(1)

        except Exception as e:
            print("Error: ", e)



if __name__ == "__main__":
   main()



        