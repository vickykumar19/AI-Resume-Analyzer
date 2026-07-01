import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI-powered feedback.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.success("Resume uploaded successfully!")
    st.text_area("Extracted Resume Text", text, height=300)
    if st.button("Analyze Resume"):
        prompt = f"""
        Analyze this resume.

        Give:
        1. ATS score out of 100 
        2. Resume summary
        3. Strengths
        4. Missing Skills
        5. Improvement suggestions

        Resume:
        {text}
        """

        response = model.generate_content(prompt)

        st.subheader("AI Analysis")
        st.write(response.text)