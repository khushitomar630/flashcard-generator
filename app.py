import streamlit as st
import openai
from utils import read_pdf, read_txt

openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")
 # store your key in .streamlit/secrets.toml
if not openai.api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

st.title("📚 LLM-Powered Flashcard Generator")

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

if st.button("Generate Flashcards") and raw_text:
    with st.spinner("Generating..."):
        system_prompt = (
            f"You are a helpful AI that generates flashcards from {subject} content. "
            f"Provide a list of at least 10 Q&A flashcards based on the given content."
        )
        user_prompt = f"Content:\n{raw_text[:3000]}"  # Truncate for token limits

        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

        output = response['choices'][0]['message']['content']
        st.markdown("### 🧠 Generated Flashcards")
        st.text_area("Q&A Flashcards", value=output, height=400)

        if st.download_button("Download as TXT", output, file_name="flashcards.txt"):
            st.success("Download Ready!")
