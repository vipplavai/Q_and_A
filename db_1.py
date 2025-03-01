import pymongo
import urllib.parse
import os

# MongoDB Credentials
username = "prashanth01071995"
password = "pradsml@2025"  # Replace with actual password

# Encode special characters in the password
encoded_password = urllib.parse.quote_plus(password)

# Modify Connection String (Disable TLS Verification)
MONGO_URI = f"mongodb+srv://{username}:{encoded_password}@cluster0.fsbic.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["Q_and_A"]  # Use your actual database name
collection = db["content_data"]  # Collection name

# Test Connection
try:
    client.admin.command('ping')  # Quick test to ensure connection
    print("✅ MongoDB Connection Successful!")
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("❌ MongoDB Connection Failed:", e)
