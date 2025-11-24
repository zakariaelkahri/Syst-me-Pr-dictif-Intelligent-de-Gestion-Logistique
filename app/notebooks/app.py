import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

import pandas as pd

# ---------------------------------------------------------------
# 1. Start Spark Session
# ---------------------------------------------------------------
@st.cache_resource
def load_spark():
    return SparkSession.builder \
        .appName("LateDeliveryPredictor") \
        .master("local[*]") \
        .getOrCreate()

spark = load_spark()

# ---------------------------------------------------------------
# 2. Load your saved PipelineModel
# ---------------------------------------------------------------
@st.cache_resource
def load_model():
    cv_model = CrossValidatorModel.load("./models/gbt_model")

    return cv_model.bestModel

model = load_model()

st.title("📦 Late Delivery Prediction App")
st.write("Fill in order details to predict late delivery risk.")

# ---------------------------------------------------------------
# 3. Create user input form
# ---------------------------------------------------------------
type_ = st.selectbox("Type", ["TRANSFER", "CASH", "PAYMENT", "DEBIT"])
days_ship = st.number_input("Days for shipment (scheduled)", min_value=1, step=1)
category_id = st.number_input("Category Id", min_value=1, step=1)
customer_segment = st.selectbox("Customer Segment", ["Consumer", "Home Office", "Corporate"])
order_qty = st.number_input("Order Item Quantity", min_value=1, step=1)
order_region = st.selectbox("Order Region", [
    "Canada", "Caribbean", "Central Africa", "Central America", "Central Asia", 
    "East Africa", "East of USA", "Eastern Asia", "Eastern Europe", "North Africa", 
    "Northern Europe", "Oceania", "South America", "South Asia", "South of  USA ", 
    "Southeast Asia", "Southern Africa", "Southern Europe", "US Center ", 
    "West Africa", "West Asia", "West of USA ", "Western Europe"
])
order_month = st.number_input("Order Month", min_value=1, max_value=12, step=1)

# ---------------------------------------------------------------
# 4. Convert to Spark DataFrame for prediction
# ---------------------------------------------------------------
input_dict = {
    "Type": type_,
    "Days for shipment (scheduled)": int(days_ship),
    "Category Id": int(category_id),
    "Customer Segment": customer_segment,
    "Order Item Quantity": int(order_qty),
    "Order Region": order_region,
    "order_month": int(order_month),
}

if st.button("Predict Late Delivery"):
    pdf = pd.DataFrame([input_dict])
    sdf = spark.createDataFrame(pdf)

    # -----------------------------------------------------------
    # 5. Predict with your full pipeline (indexers + encoder + GBT)
    # -----------------------------------------------------------
    preds = model.transform(sdf)
    result = preds.select("prediction").collect()[0][0]

    if result == 1.0:
        st.error("🔴 High risk of late delivery!")
    else:
        st.success("🟢 Delivery on time.")