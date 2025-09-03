# 🌦️ Weather Forecast Management API  

A FastAPI application to **fetch, store, and benchmark weather forecasts** using both **SQL (PostgreSQL/MySQL/SQLite)** and **MongoDB**.  

This project demonstrates:  
✅ Building APIs with FastAPI  
✅ Using Pydantic for request validation  
✅ SQLAlchemy ORM with relational DB  
✅ MongoDB integration with indexes  
✅ Benchmarking queries across SQL vs Mongo  
✅ Clean, modular architecture (services, routers, models, DB layers)

---

## 🚀 Features
- Fetch weather forecasts from **OpenWeather API** (next 24 hours in 3-hour intervals).  
- Save forecasts into **SQL + MongoDB** simultaneously.  
- Manage saved reports via CRUD endpoints (file + DB).  
- Benchmark SQL vs Mongo query performance.  
- Well-documented and production-ready codebase.  

---


## 🏗️ Project Structure
```
app/
 ├── api/
 │   ├── models.py          # Pydantic request models
 │   ├── services.py        # Weather API + file storage logic
 │   └── weather_router.py  # FastAPI routes
 ├── db/
 │   ├── sql_db.py          # SQLAlchemy engine + session
 │   ├── sql_model.py       # SQLAlchemy ORM models
 │   └── mongo_db.py        # MongoDB connection + indexes
 └── main.py                # App entrypoint
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/weather-api.git
cd weather-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_openweather_api_key
MONGO_URI=your_mongodb_connection_string
```

### 5. Run the FastAPI app
```bash
uvicorn app.main:app --reload
```

### 6. Open API docs
Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 API Endpoints

### Health Check
`GET /`  
```json
{"message": "Weather API is running"}
```

### Fetch Weather
- `GET /weather/{city}` → Fetch forecast for one city (live from API).  
- `POST /weather/multiple` → Fetch forecast for multiple cities.  

### Save Reports
- `POST /weather/save` → Save forecast to local JSON file.  
- `POST /weather/save/{city}` → Save forecast into **SQL + MongoDB**.  

### Manage Reports
- `GET /reports` → Load all saved reports (file).  
- `DELETE /reports/{city}` → Delete a saved report (file).  

### Benchmark
- `GET /benchmark/{city}` → Compare SQL vs Mongo query time.  

---

## 🗄️ Databases

### SQL (Relational DB)
- ORM model: `WeatherForecast`
- Columns: `id, city, time, temperature, description`
- Auto-created tables on startup.

### MongoDB
- Database: `weather_db`
- Collection: `weather_forecast`
- Indexes:
  - `city` (single field)  
  - `city + time` (compound index for faster queries)  

---

## 📊 Example Usage

**Fetch & Save Weather (SQL + Mongo)**  
```bash
curl -X POST "http://127.0.0.1:8000/weather/save/London"
```
Response:
```json
{
  "message": "Saved 1 day forecast for London",
  "records": 8
}
```

**Benchmark Query**  
```bash
curl "http://127.0.0.1:8000/benchmark/London"
```
Response:
```json
{
  "sql_time": "0.012345 sec",
  "mongo_time": "0.004321 sec",
  "sql_records": 8,
  "mongo_records": 8
}
```

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – API framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for relational DB  
- [MongoDB](https://www.mongodb.com/) – NoSQL database  
- [Pydantic](https://docs.pydantic.dev/) – Data validation  
- [Uvicorn](https://www.uvicorn.org/) – ASGI server  
- [OpenWeather API](https://openweathermap.org/api) – Weather data  

---

## 🎯 Future Improvements
- Add authentication (JWT)  
- Dockerize the project  
- Add caching (Redis) for faster responses  
- Extend to multi-day forecasts  
- Deploy to AWS/GCP/Azure  

---

