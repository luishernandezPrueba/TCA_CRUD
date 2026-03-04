import sys
import os
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from sqlalchemy import create_engine, text
from models import Base
from dotenv import load_dotenv

load_dotenv()

def init_db():
    DATABASE_URL = os.getenv("MYSQL_URL") or os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("No database URL found. Set MYSQL_URL or DATABASE_URL.")
    
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+asyncmy://", 1)
    
    sync_url = DATABASE_URL.replace('mysql+asyncmy://', 'mysql+pymysql://')
    

    parts = sync_url.rsplit('/', 1)
    base_url = parts[0]
    db_name = parts[1].split('?')[0] if len(parts) > 1 else 'students'  
    

    engine = create_engine(base_url)

    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()
        print(f"Database '{db_name}' ensured")
    
    # Now create tables in the actual database
    table_engine = create_engine(sync_url)
    Base.metadata.create_all(table_engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    init_db()