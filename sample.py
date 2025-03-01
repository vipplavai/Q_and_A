import pymongo
import streamlit as st

st.title("🔗 MongoDB Connection Test")

# Retrieve MongoDB URI from Streamlit Secrets
if "MONGO_URI" not in st.secrets:
    st.error("❌ MongoDB URI is missing! Add it in Streamlit Secrets.")
    st.stop()

MONGO_URI = st.secrets["MONGO_URI"]

# Test MongoDB Connection
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["Q_and_A"]  # Your database name
    collection = db["content_data"]  # Collection name
    client.admin.command('ping')  # Quick test to ensure connection
    st.success("✅ MongoDB Connection Successful!")

    # Fetch Last Entry
    last_entry = collection.find_one({}, sort=[("content_id", pymongo.DESCENDING)])
    if last_entry:
        st.write("📌 **Last Entry in Database:**", last_entry)
    else:
        st.write("⚠️ No data found in the collection!")

except pymongo.errors.ServerSelectionTimeoutError:
    st.error("❌ Could not connect! Check MongoDB URI and Network Settings.")
except pymongo.errors.InvalidURI:
    st.error("❌ Invalid MongoDB URI! Check secrets formatting.")
