import streamlit as st
import pymongo
import os

st.title("🔗 Simple MongoDB Connection Tool")

# MongoDB Connection (Replace with your URI)
MONGO_URI = st.text_input("Enter MongoDB Connection String:", type="password")
connect_button = st.button("Connect to MongoDB")

if connect_button and MONGO_URI:
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["test_database"]  # Change database name if needed
        collection = db["test_collection"]  # Change collection name if needed

        # Test Connection
        client.admin.command('ping')
        st.success("✅ MongoDB Connection Successful!")

        # Insert Sample Data
        if st.button("Insert Sample Data"):
            sample_data = {"name": "Test Entry", "value": 42}
            collection.insert_one(sample_data)
            st.success("✅ Sample Data Inserted!")

        # Fetch & Display Data
        st.subheader("📂 Stored Data")
        all_data = list(collection.find({}, {"_id": 0}))  # Hide `_id` for simplicity
        if all_data:
            st.write(all_data)
        else:
            st.write("⚠️ No data found in the database!")

    except pymongo.errors.ServerSelectionTimeoutError:
        st.error("❌ Failed to connect! Check MongoDB URI and Network Settings.")
