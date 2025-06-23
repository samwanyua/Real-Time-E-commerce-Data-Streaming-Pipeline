from faker import Faker 
from confluent_kafka import SerializingProducer  # Kafka producer with serialization support
import random 
from datetime import datetime  
import time  # For sleep/delay
import json  # To convert Python dicts to JSON strings

# Create a Faker instance
fake = Faker()

# Function to generate a random fake sales transaction
def generate_sales_transactions():
    user = fake.simple_profile()  # Generate a fake user profile

    return {
        "transaction_id": fake.uuid4(),  # Unique transaction ID
        "process_id": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "product_name": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        "product_category": random.choice(['electronics', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        "product_price": round(random.uniform(10, 1000), 2),  # Random float between 10 and 1000
        "product_quantity": random.randint(1, 10),  # Quantity between 1 and 10
        "product_brand": random.choice(['Apple', 'Samsung', 'mi', 'dell', 'sony']),
        "currency": random.choice(['USD', 'GBP']),
        "customer_id": user['username'],  # Fake customer ID (username)
        "transaction_date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',  # Current timestamp in ISO format
        "payment_method": random.choice(['Credit card', 'Debit Card', 'Online transfer'])  # Random payment type
    }

# Kafka delivery callback to report success or failure
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")  # Report topic and partition

# Main producer logic
def main():
    topic = 'financial_transactions'  # Kafka topic to produce to

    # Create Kafka producer with bootstrap server address
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })

    # Start time to run the loop for 120 seconds
    current_time = datetime.now()

    while (datetime.now() - current_time).total_seconds() < 120:
        try:
            # Generate a fake transaction
            transaction = generate_sales_transactions()

            # Add total amount (price * quantity)
            transaction['total_amount'] = transaction['product_price'] * transaction['product_quantity']

            print(transaction)

            # Produce the message to Kafka
            producer.produce(
                topic,
                key=transaction['transaction_id'],  # Unique key for partitioning
                value=json.dumps(transaction),      # Serialize to JSON string
                on_delivery=delivery_report         # Set delivery callback
            )

            producer.poll(0)  # Trigger delivery report callbacks
            time.sleep(5)  # Wait 5 seconds before producing the next transaction

        except BufferError:
            print("Buffer full! Waiting...")
            time.sleep(2)

        except Exception as e:
            # Catch-all for any unexpected errors
            print("Error: ", e)

if __name__ == "__main__":
    main()
