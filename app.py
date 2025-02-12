from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# PostgreSQL Database URL from Render
DATABASE_URL = "postgresql://sensor_user:3el9ud0KKAEkPPpeTbPFYbULSZbPiz0U@dpg-cumf5upu0jms73e0m42g-a.oregon-postgres.render.com/sensor_db_h5nk"

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Define Data Model
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

# API to Insert Data
@app.post("/insert_data")
def insert_data(data: SensorData):
    query = """
    INSERT INTO sensor_data (temperature, humidity, mq2_analog, mq2_digital, sound_analog, sound_digital, mq9_analog, mq9_digital, mq8_analog, mq8_digital, dust_density_pm25, dust_density_pm10) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data.temperature, data.humidity, data.mq2_analog, data.mq2_digital,
        data.sound_analog, data.sound_digital, data.mq9_analog, data.mq9_digital,
        data.mq8_analog, data.mq8_digital, data.dust_density_pm25, data.dust_density_pm10
    )
    cursor.execute(query, values)
    conn.commit()
    return {"message": "Data inserted successfully"}

# Run FastAPI locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
