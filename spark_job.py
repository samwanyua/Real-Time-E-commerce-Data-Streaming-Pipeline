from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

# Define schema matching your transaction data
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

# Start Spark session
spark = SparkSession.builder \
    .appName("KafkaToPostgresAndElasticsearch") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "financial_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Extract JSON
parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write batch function
def write_to_pg_and_es(df, epoch_id):
    try:
        if df.rdd.isEmpty():
            print(f"🕐 Epoch {epoch_id}: No records.")
            return

        print(f"✅ Epoch {epoch_id}: Writing {df.count()} records")
        df.printSchema()

        # Write to PostgreSQL
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/ecommerce") \
            .option("driver", "org.postgresql.Driver") \
            .option("dbtable", "transactions") \
            .option("user", "postgres") \
            .option("password", "postgres") \
            .mode("append") \
            .save()

        # Write to Elasticsearch
        df.write \
            .format("org.elasticsearch.spark.sql") \
            .option("es.nodes", "es-container") \
            .option("es.port", "9200") \
            .option("es.nodes.wan.only", "false") \
            .mode("append") \
            .save("transactions-index")

    except Exception as e:
        print(f"🔥 Error in foreachBatch: {e}")

# Start stream
query = parsed_df.writeStream \
    .foreachBatch(write_to_pg_and_es) \
    .outputMode("append") \
    .start()

query.awaitTermination()
