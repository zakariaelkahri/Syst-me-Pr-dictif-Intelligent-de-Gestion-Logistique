# fastapi/app.py
from fastapi import FastAPI, WebSocket
import socket
import asyncio
import json
import random
import threading

app = FastAPI()

# Random data options
types = ["TRANSFER", "CASH", "PAYMENT", "DEBIT"]
days_ship = list(range(1,5))
category_id = list(range(2,77))
customer_segment = ["Consumer", "Home Office", "Corporate"]
order_qty = list(range(1,6))
order_region = [
    "Canada", "Caribbean", "Central Africa", "Central America",
    "Central Asia", "East Africa", "Eastern Asia"
]
order_month = list(range(1,13))

# Spark connection (Docker network)
spark_conn = None

def start_socket_server():
    global spark_conn
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))
    server.listen(1)
    print("Socket server listening on port 9999")
    while True:
        try:
            conn, addr = server.accept()
            print(f"Spark connected from {addr}")
            spark_conn = conn
        except Exception as e:
            print(f"Socket accept error: {e}")

# Start the server in a background thread
threading.Thread(target=start_socket_server, daemon=True).start()

async def send_to_spark(data: dict):
    global spark_conn
    if spark_conn:
        try:
            spark_conn.send((json.dumps(data) + "\n").encode())
        except Exception as e:
            print(f"Error sending to Spark: {e}")
            spark_conn = None
    else:
        # print("No Spark connection available")
        pass
    

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = {
                "Type": random.choice(types),
                "Days for shipment (scheduled)": random.choice(days_ship),
                "Category Id": random.choice(category_id),
                "Customer Segment": random.choice(customer_segment),
                "Order Item Quantity": random.choice(order_qty),
                "Order Region": random.choice(order_region),
                "order_month": random.choice(order_month)
            }

            await send_to_spark(data)
            await websocket.send_text(f"Sent to Spark: {data}")
            await asyncio.sleep(1)

    except Exception as e:
        print("WebSocket error:", e)
