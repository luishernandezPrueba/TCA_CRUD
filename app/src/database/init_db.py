import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from sqlalchemy import create_engine, text
from models import Base
from database.database import DATABASE_URL

def init_db():
    # Parse the DATABASE_URL to create a connection without the database name
    sync_url = DATABASE_URL.replace('mysql+asyncmy://', 'mysql+pymysql://')
    
    # Split the URL to get the base URL without database name
    parts = sync_url.rsplit('/', 1)
    base_url = parts[0]
    db_name = parts[1] if len(parts) > 1 else 'students'
    
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