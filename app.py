from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import PyPDF2
import docx
from io import BytesIO

# Load environment variables
load_dotenv()

# Load API Key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini model and get response
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input_text])
    return response.text

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from Word file
def extract_text_from_word(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to handle file upload and text extraction
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_word(uploaded_file)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or Word file.")
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="AI-Powered Resume Extraction System", page_icon=":guardsman:", layout="wide")

# Add custom styles for better appearance
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f7f6;
        color: #333;
    }
    h1 {
        color: #5D4037;
        text-align: center;
        font-size: 3em;
        margin-top: 50px;
    }
    .stButton button {
        background-color: #FF7043;
        color: white;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #FF5722;
    }
    .stFileUploader {
        border: 2px solid #FF7043;
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        font-size: 16px;
        width: 100%;
        text-align: center;
    }
    .stFileUploader input[type="file"] {
        background-color: transparent;
        padding: 10px;
        font-size: 16px;
        width: 90%;
    }
    .stTextInput input {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        width: 100%;
    }
    .stTextArea textarea {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        width: 100%;
    }
    .stWrite {
        font-size: 18px;
        color: #5D4037;
        line-height: 1.6;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display header
st.header("AI-Powered Resume Categorization")

# User Input section
st.subheader("Upload Your esume ")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF or Word file...", type=["pdf", "docx"])

# Additional Instructions (optional)
input_prompt = st.text_input("Enter additional instructions (optional):", key="input")

# Submit Button
submit = st.button("Categorize Resume")

# Default System Prompt
system_prompt = """
You are an expert in analyzing resumes. 
You will receive a resume in text format extracted from a PDF or Word document. 
Analyze the text and predict its corresponding job category, such as Software Developer, Data Scientist, HR, Marketing, etc.
Provide a brief justification for your prediction.
"""

# Main logic for handling file submission
if submit:
    try:
        # Extract text from the uploaded file
        extracted_text = extract_text_from_file(uploaded_file)

        # Combine user input and system prompt
        final_prompt = f"{system_prompt}\n\nAdditional Instructions: {input_prompt}"

        # Pass the extracted text to Gemini for prediction
        response = get_gemini_response(extracted_text, final_prompt)

        # Display the prediction and response
        st.subheader("Predicted Job Category and Analysis:")
        st.write(response)

    except Exception as e:
        st.error(f"An error occurred: {e}")
