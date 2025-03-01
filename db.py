import pymongo
import urllib.parse

# MongoDB Credentials
username = "prashanth01071995"
password = "pradsml@2025"  # Replace with actual password

# Encode special characters in the password
encoded_password = urllib.parse.quote_plus(password)

# MongoDB Connection URI
MONGO_URI = f"mongodb+srv://{username}:{encoded_password}@cluster0.fsbic.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["Q_and_A"]  # Use your actual database name
collection = db["content_data"]  # Collection name

# Function to generate next unique content ID
def get_next_content_id():
    last_entry = collection.find_one({}, sort=[("content_id", pymongo.DESCENDING)])

    if last_entry and "content_id" in last_entry:
        try:
            last_id = int(last_entry["content_id"])  # Convert to int only if it's numeric
            new_id = f"{last_id + 1:06d}"  # Increment and format as 6-digit number
        except ValueError:
            new_id = "000001"  # Reset to 000001 if non-numeric content_id exists
    else:
        new_id = "000001"  # Start from 000001 if no entries exist
    
    return new_id
