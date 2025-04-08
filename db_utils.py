"""
Database utility functions for handling connections and errors.
"""
import os
import logging
from functools import wraps
import time
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_url():
    """
    Get the database URL from environment variables with fallback to a default SQLite database.
    """
    db_user = os.environ.get('DB_USER', '')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'sesame')
    
    # If any of the required PostgreSQL parameters are missing, use SQLite
    if not all([db_user, db_password, db_host, db_port, db_name]):
        logger.warning("Database connection parameters incomplete, using SQLite database")
        return 'sqlite:///sesame.db'
    
    # Use SQLAlchemy 2.0 compatible URL format
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def create_engine_with_retry(max_retries=3, retry_interval=2):
    """
    Create a SQLAlchemy engine with retry logic.
    
    Args:
        max_retries (int): Maximum number of connection attempts
        retry_interval (int): Seconds to wait between retries
        
    Returns:
        sqlalchemy.engine.Engine: Database engine
    """
    db_url = get_db_url()
    
    for attempt in range(max_retries):
        try:
            # Create engine with SQLAlchemy 2.0 compatible parameters
            engine = sqlalchemy.create_engine(
                db_url,
                pool_pre_ping=True,  # Check connection before using from pool
                pool_recycle=3600,   # Recycle connections after 1 hour
                future=True          # Use SQLAlchemy 2.0 API
            )
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
                
            logger.info("Database connection established successfully")
            return engine
            
        except SQLAlchemyError as e:
            logger.warning(f"Database connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error("All database connection attempts failed")
                raise
    
    # This should never be reached due to the raise in the loop
    return None

def with_db_error_handling(func):
    """
    Decorator to handle database errors gracefully.
    
    Args:
        func: The function to decorate
        
    Returns:
        Decorated function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            logger.error(f"Database operational error: {str(e)}")
            # Handle connection issues
            raise RuntimeError(f"Database connection error: {str(e)}")
        except DatabaseError as e:
            logger.error(f"Database error: {str(e)}")
            # Handle other database errors
            raise RuntimeError(f"Database error: {str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {str(e)}")
            # Handle general SQLAlchemy errors
            raise RuntimeError(f"Database query error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during database operation: {str(e)}")
            raise
    
    return wrapper
