from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml.tuning import CrossValidatorModel 
import pyspark.ml.functions as f
import os
import sys

def create_spark_session():
    return SparkSession.builder \
        .appName("LogisticsPredictionStreaming") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    print("Spark Streaming Application Started...")

    # Define schema (matching your notebook)
    schema = StructType([
        StructField("Type", StringType()),
        StructField("Days for shipment (scheduled)", IntegerType()),
        StructField("Category Id", IntegerType()),
        StructField("Customer Segment", StringType()),
        StructField("Order Item Quantity", IntegerType()),
        StructField("Order Region", StringType()),
        StructField("order_month", IntegerType())    
    ])

    # Read from socket (Update host/port via env vars for Docker)
    # In Docker, 'host' should be the service name sending data, or 'host.docker.internal' for local testing
    host = os.getenv("STREAM_HOST", "localhost") 
    port = int(os.getenv("STREAM_PORT", "9999"))

    print(f"Listening on {host}:{port}")

    model_path = "../app/notebooks/models/gbt_model"
    try:
        model = CrossValidatorModel.load(model_path).bestModel
        print("Model loaded successfully.")
        raw_df = spark.readStream \
            .format("socket") \
            .option("host", host) \
            .option("port", port) \
            .load()

        # Parse JSON
        json_df = raw_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

        predictions_df = model.transform(json_df)
        
        output_df = predictions_df.select(
            col("Type"),
            col("Days for shipment (scheduled)"),
            col("prediction").alias("Late Delivery Prediction")
        )
        # Simple console output for verification
        query = output_df.writeStream \
            .outputMode("append") \
            .format("console") \
            .trigger(processingTime='0 seconds')\
            .start()

        query.awaitTermination()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()