from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

# Define the schema
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("process_id", StringType()) \
    .add("product_name", StringType()) \
    .add("product_category", StringType()) \
    .add("product_price", FloatType()) \
    .add("product_quantity", IntegerType()) \
    .add("total_amount", FloatType()) \
    .add("product_brand", StringType()) \
    .add("currency", StringType()) \
    .add("customer_id", StringType()) \
    .add("transaction_date", StringType()) \
    .add("payment_method", StringType())

# Create Spark session
spark = SparkSession.builder \
    .appName("EcommerceTransactionStreaming") \
    .getOrCreate()

# Read from Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "financial_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Convert the Kafka value to string and parse the JSON
df_value = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Optional: Print the schema to verify
df_value.printSchema()

# Define the batch writer for PostgreSQL
def write_to_postgres(batch_df, epoch_id):
    try:
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/ecommerce") \
            .option("dbtable", "transactions") \
            .option("user", "postgres") \
            .option("password", "postgres") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
        print(f"✅ Batch {epoch_id} written to PostgreSQL.")
    except Exception as e:
        print(f"❌ Error writing batch {epoch_id} to PostgreSQL: {e}")

# Write stream to PostgreSQL
postgres_stream = df_value.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

# Write stream to Elasticsearch
es_stream = df_value.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("es.nodes", "es-container") \
    .option("es.port", "9200") \
    .option("es.resource", "sales-agg/_doc") \
    .start()

# Wait for both to terminate
postgres_stream.awaitTermination()
es_stream.awaitTermination()
