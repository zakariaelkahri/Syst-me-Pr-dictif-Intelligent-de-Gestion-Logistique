import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField


spark = SparkSession.builder.appName("logistic_prediction").getOrCreate()

