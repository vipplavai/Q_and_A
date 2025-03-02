from flask import Flask, request, jsonify
import pymongo
import os

app = Flask(__name__)

# Load MongoDB URI from Environment Variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://prashanth01071995:pradsml%402025@cluster0.fsbic.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connect to MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["Q_and_A"]
    collection = db["content_data"]
    client.admin.command('ping')  # Test Connection
    print("✅ Connected to MongoDB Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed! Error: {e}")

# API: Fetch content by ID
@app.route('/get_content/<content_id>', methods=['GET'])
def get_content(content_id):
    content_data = collection.find_one({"content_id": content_id}, {"_id": 0})
    if content_data:
        return jsonify({"status": "success", "data": content_data})
    return jsonify({"status": "error", "message": "Content not found"}), 404

# API: Add question to content
@app.route('/add_question', methods=['POST'])
def add_question():
    data = request.json
    content_id = data.get("content_id")
    question_text = data.get("question")
    difficulty = data.get("difficulty", "medium")

    if not content_id or not question_text:
        return jsonify({"status": "error", "message": "Missing content_id or question"}), 400

    collection.update_one(
        {"content_id": content_id},
        {"$push": {"questions": {"question": question_text, "difficulty": difficulty, "answer": ""}}},
        upsert=True
    )
    return jsonify({"status": "success", "message": "Question added successfully!"})

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
