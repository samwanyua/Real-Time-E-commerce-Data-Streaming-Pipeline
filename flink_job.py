from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.jdbc import JdbcSink

import json

def map_transaction(record):
    data = json.loads(record)
    return (
        data['transaction_id'],
        data['process_id'],
        data['product_name'],
        data['product_category'],
        float(data['product_price']),
        int(data['product_quantity']),
        float(data['total_amount']),
        data['product_brand'],
        data['currency'],
        data['customer_id'],
        data['transcation_date'],
        data['payment_method']
    )

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# Set up Kafka consumer
kafka_props = {
    'bootstrap.servers': 'broker:29092',
    'group.id': 'flink-consumer-group'
}

consumer = FlinkKafkaConsumer(
    topics='financial_transactions',
    deserialization_schema=SimpleStringSchema(),
    properties=kafka_props
)

# Create a stream from Kafka
stream = env.add_source(consumer).map(
    map_transaction,
    output_type=Types.TUPLE([
        Types.STRING(),  # transaction_id
        Types.STRING(),  # process_id
        Types.STRING(),  # product_name
        Types.STRING(),  # product_category
        Types.FLOAT(),   # product_price
        Types.INT(),     # product_quantity
        Types.FLOAT(),   # total_amount
        Types.STRING(),  # product_brand
        Types.STRING(),  # currency
        Types.STRING(),  # customer_id
        Types.STRING(),  # transaction_date
        Types.STRING()   # payment_method
    ])
)

# Define JDBC sink to Postgres
sink = JdbcSink.sink(
    sql="""
        INSERT INTO transactions (
            transaction_id, process_id, product_name, product_category,
            product_price, product_quantity, total_amount, product_brand,
            currency, customer_id, transaction_date, payment_method
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (transaction_id) DO NOTHING
    """,
    type_information=Types.TUPLE([
        Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(),
        Types.FLOAT(), Types.INT(), Types.FLOAT(), Types.STRING(),
        Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()
    ]),
    driver_class_name='org.postgresql.Driver',
    jdbc_url='jdbc:postgresql://postgres_ecommerce:5432/postgres',
    username='postgres',
    password='postgres'
)

# Attach sink to stream
stream.add_sink(sink)

# Execute the Flink job
env.execute("Kafka to Postgres Transaction Pipeline")
