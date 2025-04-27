import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

MYSQL_URL = "mysql+pymysql://root@mysql:3306/sql_injection"

# Retry connection
for i in range(10):
    try:
        engine = create_engine(MYSQL_URL)
        engine.connect()
        break
    except OperationalError:
        print("❗ Waiting for MySQL to be ready...")
        time.sleep(3)
else:
    raise Exception("🚫 Failed to connect to MySQL after multiple retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
