from faker import Faker 
from confluent_kafka import Producer  # <-- Use basic Producer
import random 
from datetime import datetime  
import time
import json

fake = Faker()

def generate_sales_transactions():
    user = fake.simple_profile()

    return {
        "transaction_id": fake.uuid4(),
        "process_id": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "product_name": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        "product_category": random.choice(['electronics', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        "product_price": round(random.uniform(10, 1000), 2),
        "product_quantity": random.randint(1, 10),
        "product_brand": random.choice(['Apple', 'Samsung', 'mi', 'dell', 'sony']),
        "currency": random.choice(['USD', 'GBP']),
        "customer_id": user['username'],
        "transaction_date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "payment_method": random.choice(['Credit card', 'Debit Card', 'Online transfer'])
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

def main():
    topic = 'financial_transactions'

    # ✅ Basic Producer without serializers
    producer = Producer({
        'bootstrap.servers': 'broker:29092'
    })

    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < 240:
        try:
            transaction = generate_sales_transactions()
            transaction['total_amount'] = transaction['product_price'] * transaction['product_quantity']

            print(f"Producing: {transaction}")

            producer.produce(
                topic,
                key=transaction['transaction_id'],
                value=json.dumps(transaction),
                callback=delivery_report
            )
            producer.poll(0)
            time.sleep(5)

        except BufferError:
            print("⛔ Buffer full! Retrying...")
            time.sleep(2)
        except Exception as e:
            print("🔥 Error: ", e)

    producer.flush()

if __name__ == "__main__":
    main()
