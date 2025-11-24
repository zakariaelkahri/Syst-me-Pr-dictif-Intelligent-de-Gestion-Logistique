# streamlit/spark_stream.py
import socket
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml.tuning import CrossValidatorModel

# Spark session
spark = SparkSession.builder.appName("StreamlitSpark").getOrCreate()

# Schema
schema = StructType([
    StructField("Type", StringType(), True),
    StructField("Days for shipment (scheduled)", IntegerType(), True),
    StructField("Category Id", IntegerType(), True),
    StructField("Customer Segment", StringType(), True),
    StructField("Order Item Quantity", IntegerType(), True),
    StructField("Order Region", StringType(), True),
    StructField("order_month", IntegerType(), True)
])

# Load your trained Spark ML model
model = CrossValidatorModel.load("./models/gbt_model")

# TCP socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8888))
server_socket.listen(1)
print("Waiting for FastAPI connection...")

conn, addr = server_socket.accept()
print("Connected by", addr)

buffer = ""
while True:
    data = conn.recv(1024)
    if not data:
        break
    buffer += data.decode()
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        record = json.loads(line)
        print(json.loads(line))
        df = spark.createDataFrame([record], schema=schema)
        preds = model.transform(df)
        preds.show()

