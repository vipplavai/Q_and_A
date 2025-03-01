import streamlit as st
from db import collection

st.title("📝 Direct Question Entry Tool")

# Input for Content ID
content_id_input = st.text_input("Enter Content ID to Fetch Content (e.g., 000001):")

# Initialize session state for tracking edits
if "editing_question_index" not in st.session_state:
    st.session_state.editing_question_index = None  # No active edit initially

if content_id_input:
    content_data = collection.find_one({"content_id": content_id_input})

    if content_data:
        st.subheader("📖 Fetched Content")
        st.info(content_data["content"])

        # Show Total Questions Count
        total_questions = len(content_data.get("questions", []))
        st.write(f"📌 **Total Questions Added:** {total_questions}")

        # Display Existing Questions & Allow Editing
        if total_questions > 0:
            st.write("📋 **Existing Questions:**")
            for index, q in enumerate(content_data["questions"], start=1):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.write(f"{index}. **{q['question']}** ({q['difficulty'].capitalize()})")

                with col2:
                    if st.button(f"✏️ Edit", key=f"edit_{index}"):
                        st.session_state.editing_question_index = index - 1  # Set question index for editing
                        st.rerun()

        # Handle Question Editing
        if st.session_state.editing_question_index is not None:
            st.subheader("✏️ Edit Question")
            edit_index = st.session_state.editing_question_index
            existing_question = content_data["questions"][edit_index]

            new_question_text = st.text_area("Edit Question:", existing_question["question"], height=100)
            new_difficulty = st.selectbox(
                "Edit Difficulty Level:",
                ["easy", "medium", "hard"],
                index=["easy", "medium", "hard"].index(existing_question["difficulty"])
            )

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Save Changes"):
                    collection.update_one(
                        {"content_id": content_id_input},
                        {"$set": {f"questions.{edit_index}": {
                            "question": new_question_text,
                            "difficulty": new_difficulty,
                            "answer": existing_question.get("answer", "")
                        }}}  
                    )
                    st.session_state.editing_question_index = None  # Reset edit state
                    st.rerun()  # Refresh to show updated data

            with col2:
                if st.button("❌ Cancel Edit"):
                    st.session_state.editing_question_index = None  # Reset edit state
                    st.rerun()

        # Add New Questions
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
                st.rerun()  # Automatically update UI
            else:
                st.error("⚠️ Please enter a question before saving!")

    else:
        st.error("❌ Invalid Content ID! No content found.")
