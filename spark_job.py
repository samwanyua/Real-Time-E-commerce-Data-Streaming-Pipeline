from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

# Define schema based on the init.sql table
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

spark = SparkSession.builder \
    .appName("EcommerceTransactionStreaming") \
    .getOrCreate()

# Read from Kafka topic
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "financial_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON from Kafka message
df_value = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Optional: Compute total_amount if not passed (commented since already computed)
# df_value = df_value.withColumn("total_amount", col("product_price") * col("product_quantity"))

# Write to PostgreSQL
def write_to_postgres(batch_df, _):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/ecommerce") \
        .option("dbtable", "transactions") \
        .option("user", "ecommerce") \
        .option("password", "ecommerce") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

df_value.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

# Write to Elasticsearch
df_value.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .option("es.nodes", "es-container") \
    .option("es.port", "9200") \
    .option("es.resource", "sales-agg/_doc") \
    .start() \
    .awaitTermination()
