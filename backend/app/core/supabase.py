import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from loguru import logger

load_dotenv()

# Supabase PostgreSQL connection
class SupabaseDB:
    def __init__(self):
        self.DATABASE_URL = settings.DATABASE_URL
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self._initialize_connection()
    
    def _initialize_connection(self):
        try:
            # Create SQLAlchemy engine
            self.engine = create_engine(
                self.DATABASE_URL,
                pool_pre_ping=True,  # Check connection before using from pool
                pool_size=10,        # Maximum number of connections in the pool
                max_overflow=20,     # Maximum number of connections that can be created beyond pool_size
                pool_recycle=3600,   # Recycle connections after 1 hour
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            logger.info("Successfully connected to Supabase PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def get_db_session(self):
        """Get a database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_tables(self):
        """Create all tables in the database"""
        try:
            self.Base.metadata.create_all(bind=self.engine)
            logger.info("Successfully created database tables")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

# Create a singleton instance
supabase_db = SupabaseDB()