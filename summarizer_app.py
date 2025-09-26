import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

🌟 App Config
st.set_page_config(page_title="📄 Summarizer Tool", page_icon="✨")
st.title("📄 Summarizer Tool ✨")
st.write("Upload a PDF or paste text/article below to get a summary 📑")

 📂 File Upload
uploaded_file = st.file_uploader("📂 Upload a PDF file", type="pdf")
input_text = st.text_area("✍️ Or paste your text/article here:")

📄 Extract PDF text
pdf_text = ""
if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""

final_text = pdf_text if pdf_text else input_text

 🚀 Load summarizer once
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="t5-small")  # lightweight model

summarizer = load_summarizer()

🚀 Summarize Button
if st.button("✨ Summarize ✨"):
    if not final_text.strip():
        st.warning("⚠️ Please upload a PDF or paste some text.")
    else:
        with st.spinner("⏳ Summarizing..."):
            # Split into chunks to avoid memory issues
            chunk_size = 500  # smaller chunks for t5-small
            summaries = []
            for i in range(0, len(final_text), chunk_size):
                chunk = final_text[i:i+chunk_size]
                summary = summarizer(
                    chunk, max_length=100, min_length=25, do_sample=False
                )[0]['summary_text']
                summaries.append("• " + summary)

            📝 Display the final summary
            st.subheader("📌 Summary")
            st.write("\n".join(summaries))
