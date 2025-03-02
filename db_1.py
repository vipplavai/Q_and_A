import pymongo
import urllib.parse
import os

# Load MongoDB URI from Environment Variables (Render uses ENV variables)
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["Q_and_A"]  # Database Name
    collection = db["content_data"]  # Collection Name
    client.admin.command('ping')  # Test Connection
    print("✅ Connected to MongoDB Successfully!")
except pymongo.errors.ConnectionFailure:
    print("❌ Connection Failed! Check MongoDB Network Settings.")
except pymongo.errors.ConfigurationError:
    print("❌ Configuration Error! Check your MongoDB URI.")
