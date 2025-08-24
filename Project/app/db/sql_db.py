from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace root and password with your MySQL username/password
DATABASE_URL = "mysql+pymysql://root:3%40Ganesh@localhost/weather_db"


# ✅ No check_same_thread for MySQL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ✅ Add this to create all tables if they don't exist
def init_db():
    import app.db_models.sql_model  # import your models here so Base knows them
    Base.metadata.create_all(bind=engine)
