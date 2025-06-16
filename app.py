import streamlit as st
import openai
from utils import read_pdf, read_txt
from openai import OpenAI, RateLimitError

st.set_page_config(page_title="Flashcard Generator", layout="wide")

# Input for OpenAI key
openai_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=openai_key)

st.title("📚 LLM-Powered Flashcard Generator")

# Input method
input_method = st.radio("Choose Input Type", ["Upload File", "Paste Text"])
subject = st.selectbox("Select Subject (optional)", ["General", "Biology", "History", "CS", "Math"])
raw_text = ""

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a .pdf or .txt file", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            raw_text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            raw_text = read_txt(uploaded_file)
else:
    raw_text = st.text_area("Paste your educational content here", height=300)

# Generate button
if st.button("Generate Flashcards") and raw_text:
    with st.spinner("Generating..."):
        try:
            system_prompt = (
                f"You are a helpful AI that generates flashcards from {subject} content. "
                f"Provide a list of at least 10 Q&A flashcards based on the given content."
            )
            user_prompt = f"Content:\n{raw_text[:3000]}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            output = response.choices[0].message.content
            st.markdown("### 🧠 Generated Flashcards")
            st.text_area("Q&A Flashcards", value=output, height=400)

            st.download_button("Download as TXT", output, file_name="flashcards.txt")

        except RateLimitError:
            st.error("❌ Rate limit reached. Please wait or use a different API key.")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")