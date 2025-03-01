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
        client.admin.command('ping')  # Test MongoDB connection
        st.success("✅ Connected to MongoDB Successfully!")

    except pymongo.errors.ConnectionFailure:
        st.error("❌ Connection Failed! Check MongoDB Network Settings.")
    except pymongo.errors.ConfigurationError:
        st.error("❌ Configuration Error! Check your MongoDB URI.")
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
