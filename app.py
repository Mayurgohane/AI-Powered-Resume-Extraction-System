import streamlit as st
import PyPDF2
import docx
from your_resume_categorization_module import categorize_resume  # Assuming you have a function for categorization

# Title
st.title("AI-Powered Resume Categorization")

# File uploader
uploaded_file = st.file_uploader("Select a PDF or Word Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    # Process the file
    if uploaded_file.type == "application/pdf":
        # Read the PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Read the Word file
        doc = docx.Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text

    # Display the content
    st.subheader("Resume Content")
    st.text_area("Extracted Text", text, height=300)

    # Categorize the resume
    if st.button("Categorize Resume"):
        job_category = categorize_resume(text)  # Replace with your categorization logic
        st.write(f"Job Category: {job_category}")
