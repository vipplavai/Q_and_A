import streamlit as st
from db_1 import collection

st.title("📝 Direct Question Entry Tool")

# Input for Content ID
content_id_input = st.text_input("Enter Content ID to Fetch Content (e.g., 000001):")

if content_id_input:
    content_data = collection.find_one({"content_id": content_id_input})

    if content_data:
        st.subheader("📖 Fetched Content")
        st.info(content_data["content"])

        total_questions = len(content_data.get("questions", []))
        st.write(f"📌 **Total Questions Added:** {total_questions}")

        if total_questions > 0:
            st.write("📋 **Existing Questions:**")
            for index, q in enumerate(content_data["questions"], start=1):
                st.write(f"{index}. **{q['question']}** ({q['difficulty'].capitalize()})")

        st.subheader("➕ Add a New Question")
        question_text = st.text_area("Enter Question:", height=100)
        difficulty = st.selectbox("Select Difficulty Level:", ["easy", "medium", "hard"])

        if st.button("Save Question"):
            if question_text.strip():
                collection.update_one(
                    {"content_id": content_id_input},
                    {"$push": {"questions": {"question": question_text, "difficulty": difficulty, "answer": ""}}},
                    upsert=True
                )
                st.success("✅ Question saved successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please enter a question before saving!")

    else:
        st.error("❌ Invalid Content ID! No content found.")
