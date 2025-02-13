from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
import datetime

app = FastAPI()

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://shivam66jnp:XYPPYf4gyJf5El4O@cluster0.ru4bvi9.mongodb.net/esp8266_data?retryWrites=true&w=majority")
db = client["esp8266_data"]
collection = db["sensor_data"]

# Define Sensor Data Model
class SensorData(BaseModel):
    temperature: float
    humidity: float
    mq2_analog: int
    mq2_digital: int
    sound_analog: int
    sound_digital: int
    mq9_analog: int
    mq9_digital: int
    mq8_analog: int
    mq8_digital: int
    dust_density_pm25: float
    dust_density_pm10: float

@app.post("/insert")
async def insert_data(data: SensorData):
    record = data.dict()
    record["timestamp"] = datetime.datetime.utcnow()
    collection.insert_one(record)
    return {"message": "Data inserted successfully"}

@app.get("/data")
async def get_data():
    records = list(collection.find({}, {"_id": 0}))
    return {"data": records}

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}
