from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import asyncio
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set")

logger.info("MongoDB URL format validation...")
if not MONGO_URL.startswith("mongodb+srv://") and not MONGO_URL.startswith("mongodb://"):
    raise ValueError("Invalid MongoDB URL format")

try:
    logger.info("Connecting to MongoDB...")
    # Create MongoDB client with more lenient timeouts
    client = AsyncIOMotorClient(
        MONGO_URL,
        serverSelectionTimeoutMS=30000,  # 30 seconds
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        maxPoolSize=10,
        retryWrites=True
    )
    
    # Use the database name from the connection string or default to task_manager
    db_name = "task_manager"
    db = client[db_name]
    tasks_collection = db["tasks"]
    
    # Log connection details
    logger.info(f"Using database: {db_name}")
    logger.info("MongoDB connection initialized")
    
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise
