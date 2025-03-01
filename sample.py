import streamlit as st
import pymongo

st.title("🔗 MongoDB Connection Tool")

# Button to Connect to MongoDB
if st.button("Connect to MongoDB"):
    try:
        # Retrieve MongoDB URI from Streamlit Secrets
        MONGO_URI = st.secrets["MONGO_URI"]

        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["Q_and_A"]  # Database name
        collection = db["content_data"]  # Collection name

        # Test Connection
        client.admin.command('ping')
        st.success("✅ Connected to MongoDB Successfully!")

        # Display a sample document if available
        sample_data = collection.find_one({}, {"_id": 0})  # Hide `_id` for readability
        if sample_data:
            st.write("📌 **Sample Document:**", sample_data)
        else:
            st.write("⚠️ No data found in the database!")

    except pymongo.errors.ServerSelectionTimeoutError:
        st.error("❌ Could not connect! Check MongoDB URI and Network Settings.")
    except pymongo.errors.InvalidURI:
        st.error("❌ Invalid MongoDB URI! Check your Streamlit Secrets.")
