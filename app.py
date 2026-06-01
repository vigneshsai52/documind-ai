from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}

@app.route('/')
def home():
    return "Server running with FREE Groq AI!"

def extract_text(file, filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.pdf':
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text, len(pdf.pages)

    elif ext in ('.docx', '.doc'):
        import docx
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text, None

    elif ext == '.txt':
        text = file.read().decode('utf-8', errors='ignore')
        return text, None

    else:
        return None, None

def analyze_with_ai(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document analyzer. Provide: 1) Document type 2) 3 key points 3) Brief summary in simple English"
                },
                {
                    "role": "user",
                    "content": f"Analyze this document:\n\n{text[:4000]}"
                }
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis error: {str(e)}"

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type. Please upload PDF, DOCX, or TXT"}), 400

    try:
        text, pages = extract_text(file, file.filename)

        if text is None:
            return jsonify({"error": "Could not read this file type"}), 400

        if not text.strip():
            return jsonify({"error": "Could not extract text from the document"}), 400

        ai_result = analyze_with_ai(text)

        result = {
            "filename": file.filename,
            "analysis": ai_result
        }
        if pages is not None:
            result["pages"] = pages

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)