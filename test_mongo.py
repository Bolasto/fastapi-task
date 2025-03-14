import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_connection():
    load_dotenv()
    MONGO_URL = os.getenv("MONGO_URL")
    
    try:
        logger.info("Attempting to connect to MongoDB...")
        client = AsyncIOMotorClient(MONGO_URL)
        
        # Test the connection
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        
        # Try to insert a test document
        db = client.task_manager
        collection = db.test_collection
        
        result = await collection.insert_one({"test": "document"})
        logger.info(f"Successfully inserted test document with ID: {result.inserted_id}")
        
        # Clean up test document
        await collection.delete_one({"_id": result.inserted_id})
        logger.info("Successfully cleaned up test document")
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
