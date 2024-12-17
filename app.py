from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from io import BytesIO
import docx

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Function to get response from Gemini
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input_text])
    return response.text

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from Word file
def extract_text_from_word(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to handle text extraction
def extract_text(uploaded_file):
    if uploaded_file.filename.endswith(".pdf"):
        return extract_text_from_pdf(BytesIO(uploaded_file.read()))
    elif uploaded_file.filename.endswith(".docx"):
        return extract_text_from_word(BytesIO(uploaded_file.read()))
    else:
        raise Exception("Unsupported file type. Please upload a PDF or DOCX file.")

# System prompt for the Gemini model
SYSTEM_PROMPT = """
You are an expert in analyzing resumes. 
You will receive a resume in text format extracted from a PDF or Word document. 
Analyze the text and predict its corresponding job category, such as Software Developer, Data Scientist, HR, Marketing, etc.
Provide a brief justification for your prediction.
"""

# Route to display the HTML form
@app.route("/")
def home():
    return render_template("index.html")

# Route to upload file and get prediction
@app.route("/categorize-resume/", methods=["POST"])
def categorize_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Extract text
        extracted_text = extract_text(file)
        
        # Generate Gemini response
        response = get_gemini_response(extracted_text, SYSTEM_PROMPT)
        
        # Store the result and pass it to the result page
        result = {
            "filename": file.filename,
            "job_category_prediction": response
        }
        
        return render_template("result.html", result=result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
