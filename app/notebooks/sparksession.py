import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("logistic_prediction").master("local[*]") .getOrCreate()

