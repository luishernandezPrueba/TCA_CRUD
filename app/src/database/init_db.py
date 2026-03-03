import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from sqlalchemy import create_engine, text
from models import Base
from dotenv import load_dotenv

load_dotenv()

def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Handle Railway's mysql:// format
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+asyncmy://", 1)
    
    # Parse the DATABASE_URL to create a connection without the database name
    sync_url = DATABASE_URL.replace('mysql+asyncmy://', 'mysql+pymysql://')
    
    # Split the URL to get the base URL without database name
    parts = sync_url.rsplit('/', 1)
    base_url = parts[0]
    db_name = parts[1].split('?')[0] if len(parts) > 1 else 'students'  # Handle query params
    
    # Create engine for initial connection (without database)
    engine = create_engine(base_url)
    
    # Create database if it doesn't exist
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