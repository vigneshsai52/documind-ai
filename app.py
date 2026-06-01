from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import os
import json
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
    return "ContractScan API - AI Contract Analyzer running with FREE Groq AI!"

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

def analyze_contract(text):
    """Analyze contract with structured AI prompt for hiring impact"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert legal contract analyzer. Analyze the provided contract and return a structured analysis.

Your response must follow this exact format:

📋 CONTRACT TYPE
[Identify: Employment Agreement, NDA, Rental/Lease, Service Agreement, Sales Contract, Loan Agreement, Partnership Agreement, etc.]

👥 PARTIES INVOLVED
• [Party 1 name and role]
• [Party 2 name and role]

📅 KEY DATES & DEADLINES
• [Date]: [What happens on this date]
• [Date]: [Deadline or milestone]

💰 FINANCIAL TERMS
• [Payment amount, frequency, penalties, fees, etc.]

⚠️ RISKY CLAUSES (Flag anything potentially harmful)
🔴 HIGH RISK: [Clause that could cause major financial/legal problems]
🟡 MEDIUM RISK: [Clause that could be problematic]
🟢 LOW RISK: [Minor concern]

❓ MISSING STANDARD CLAUSES (What should be here but isn't)
• [Missing protection or standard term]

📝 PLAIN ENGLISH SUMMARY
[Explain this contract simply, like you're talking to a friend. What is this person actually agreeing to? What should they watch out for?]

Be thorough. Your goal is to protect the person reading this from signing something bad."""
                },
                {
                    "role": "user",
                    "content": f"Analyze this contract:\n\n{text[:6000]}"
                }
            ],
            temperature=0.3,
            max_tokens=1500
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
        return jsonify({"error": "Unsupported file type. Please upload PDF, DOCX, DOC, or TXT"}), 400

    try:
        text, pages = extract_text(file, file.filename)

        if text is None:
            return jsonify({"error": "Could not read this file type"}), 400

        if not text.strip():
            return jsonify({"error": "Could not extract text from the document. It may be scanned/image-based."}), 400

        # Check if it looks like a contract
        contract_keywords = ['agreement', 'contract', 'terms', 'parties', 'obligations', 
                           'liability', 'confidential', 'termination', 'payment', 'clause']
        text_lower = text.lower()
        is_likely_contract = any(kw in text_lower for kw in contract_keywords)

        ai_result = analyze_contract(text)

        result = {
            "filename": file.filename,
            "is_likely_contract": is_likely_contract,
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