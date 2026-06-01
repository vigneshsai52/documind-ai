# ContractScan 🔍

**AI-powered contract analyzer.** Upload any contract (PDF, DOCX, DOC, TXT) and get instant analysis of key terms, risky clauses, and a plain-English summary.

🚀 **Live Demo:** [https://documind-6kv5kn89t-documind-ai-s-projects.vercel.app](your-url)

---

## ⚡ The Problem

People sign contracts every day without understanding them:
- Employment agreements with hidden non-competes
- Rental leases with unfair penalties  
- Service contracts with auto-renewal traps
- NDAs that are way too broad

**Lawyers cost $300-500/hour.** Most people can't afford that.

---

## ✅ The Solution

ContractScan uses AI to make contract review **free and accessible**:

| Feature | What It Does |
|---------|-------------|
| 📋 **Contract Type Detection** | Identifies what kind of contract it is |
| 👥 **Party Extraction** | Who's involved and their roles |
| 📅 **Key Dates** | Deadlines, start/end dates, milestones |
| 💰 **Financial Terms** | Payments, penalties, fees, hidden costs |
| ⚠️ **Risk Detection** | Flags HIGH/MEDIUM/LOW risk clauses |
| ❓ **Missing Clauses** | Standard protections that should be there |
| 📝 **Plain English Summary** | Explains what you're actually agreeing to |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **AI Engine** | Groq API (Llama 3.1) — **FREE tier** |
| **Document Processing** | PyPDF2, python-docx |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Railway (backend), Vercel (frontend) |

---

## 📊 Example Analysis

**Input:** Employment contract PDF

**Output:**
📋 CONTRACT TYPE Employment Agreement
👥 PARTIES INVOLVED • Employee: John Doe • Employer: TechCorp Inc.
📅 KEY DATES & DEADLINES • Start Date: January 15, 2024 • Review Period: 90 days • Notice Period: 30 days
💰 FINANCIAL TERMS • Salary: $85,000/year • Bonus: Up to 10% based on performance • Health insurance: Employer pays 80%
⚠️ RISKY CLAUSES 🔴 HIGH RISK: Non-compete clause prevents working in same industry for 2 years after leaving 🟡 MEDIUM RISK: Intellectual property assignment is very broad 🟢 LOW RISK: 30-day termination notice is shorter than standard 60 days
❓ MISSING STANDARD CLAUSES • Severance package details • Remote work policy • Expense reimbursement procedure
📝 PLAIN ENGLISH SUMMARY You're agreeing to work for TechCorp for $85k/year. The big red flag is the non-compete — you can't work in tech for 2 years if you leave. Also, they own everything you create, even outside work hours. Consider negotiating these points before signing.
---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/vigneshsai52/contractscan.git
cd contractscan

# Backend setup
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python app.py

# Frontend (open index.html or use live server)

|I'll give you the full updated code to reframe this as ContractScan — AI Contract Analyzer. This is the same project, just positioned much better for hiring.
Updated app.py
Python

Copy
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
Updated index.html
Html

Copy
<!DOCTYPE html>
<html>
<head>
    <title>ContractScan - AI Contract Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        h1 { 
            font-size: 2.8rem; 
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .tagline {
            font-size: 1.2rem;
            opacity: 0.95;
            margin-bottom: 8px;
        }

        .warning {
            color: #ffd700;
            font-size: 1rem;
            font-weight: 600;
        }

        .badge {
            display: inline-block;
            background: #4ade80;
            color: #064e3b;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 12px;
        }

        .card {
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1e3a5f;
        }

        .stat-label {
            font-size: 0.85rem;
            color: #666;
        }

        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
        }

        .upload-area:hover {
            border-color: #2d5a87;
            background: #f0f7ff;
        }

        .upload-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .supported-types {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 12px;
            flex-wrap: wrap;
        }

        .type-badge {
            background: #e8f4f8;
            color: #1e3a5f;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid #cce;
        }

        input[type="file"] { display: none; }

        .btn-browse {
            background: #e8f4f8;
            color: #1e3a5f;
            padding: 10px 24px;
            border: 2px solid #2d5a87;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
            margin-top: 16px;
            display: inline-block;
        }

        .btn-browse:hover { background: #d0e8f0; }

        .btn-analyze {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
            padding: 16px 32px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            transition: transform 0.2s;
        }

        .btn-analyze:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(30, 58, 95, 0.3);
        }

        .btn-analyze:disabled { 
            opacity: 0.5; 
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #1e3a5f;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result {
            display: none;
            margin-top: 30px;
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }

        .result-header h3 {
            color: #1e3a5f;
            font-size: 1.4rem;
        }

        .contract-badge {
            background: #4ade80;
            color: #064e3b;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .not-contract-badge {
            background: #fbbf24;
            color: #92400e;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .result-box {
            background: #f8fafc;
            border-left: 4px solid #1e3a5f;
            padding: 25px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .result-box pre {
            white-space: pre-wrap;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.8;
            color: #334;
            font-size: 0.95rem;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }

        .file-name {
            color: #1e3a5f;
            font-weight: 600;
            margin-top: 10px;
            font-size: 0.95rem;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #eee;
        }

        .feature {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            color: #555;
        }

        .feature-icon {
            font-size: 1.2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📄 ContractScan</h1>
            <p class="tagline">AI-powered contract analysis. Know what you're signing.</p>
            <p class="warning">⚠️ Don't sign until you understand every clause</p>
            <span class="badge">⚡ Powered by FREE Groq AI</span>
        </header>

        <div class="card">
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Formats Supported</div>
                </div>
                <div class="stat">
                    <div class="stat-number">7</div>
                    <div class="stat-label">Analysis Points</div>
                </div>
                <div class="stat">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Free to Use</div>
                </div>
            </div>

            <div class="upload-area" id="uploadArea" onclick="document.getElementById('file').click()">
                <div class="upload-icon">📑</div>
                <h3>Upload your contract</h3>
                <p style="color: #666; margin-top: 5px;">Drag & drop or click to browse</p>

                <div class="supported-types">
                    <span class="type-badge">PDF</span>
                    <span class="type-badge">DOCX</span>
                    <span class="type-badge">DOC</span>
                    <span class="type-badge">TXT</span>
                </div>

                <p style="margin-top: 10px; font-size: 0.85rem; color: #999;">Maximum file size: 10MB</p>

                <input type="file" id="file" accept=".pdf,.docx,.doc,.txt" onchange="updateFileName()">

                <p class="file-name" id="fileName"></p>
            </div>

            <button class="btn-analyze" id="analyzeBtn" onclick="analyze()" disabled>
                🔍 Analyze Contract
            </button>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is analyzing your contract...</p>
                <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">Checking for risks, key terms, and missing clauses</p>
            </div>

            <div class="error" id="error"></div>

            <div class="result" id="result">
                <div class="result-header">
                    <h3>✅ Analysis Complete</h3>
                    <span id="contractBadge"></span>
                </div>
                <div class="result-box">
                    <pre id="analysisText"></pre>
                </div>
            </div>

            <div class="features">
                <div class="feature">
                    <span class="feature-icon">⚠️</span>
                    <span>Risk detection</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">💰</span>
                    <span>Financial terms</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">📅</span>
                    <span>Key dates</span>
                </div>
                <div class="feature">
                    <span class="feature-icon">🔍</span>
                    <span>Missing clauses</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateFileName() {
            const file = document.getElementById('file').files[0];
            if (file) {
                document.getElementById('fileName').textContent = "Selected: " + file.name;
                document.getElementById('analyzeBtn').disabled = false;
            }
        }

        async function analyze() {
            const file = document.getElementById('file').files[0];
            if (!file) return;

            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            const btn = document.getElementById('analyzeBtn');
            const contractBadge = document.getElementById('contractBadge');

            result.style.display = 'none';
            error.style.display = 'none';
            loading.style.display = 'block';
            btn.disabled = true;

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch(
                    'https://documind-ai-production-ce16.up.railway.app/analyze',
                    { method: 'POST', body: formData }
                );

                const data = await response.json();
                loading.style.display = 'none';

                if (data.error) {
                    error.textContent = '❌ ' + data.error;
                    error.style.display = 'block';
                } else {
                    document.getElementById('analysisText').textContent = data.analysis;
                    
                    // Show contract detection badge
                    if (data.is_likely_contract) {
                        contractBadge.className = 'contract-badge';
                        contractBadge.textContent = '✓ Contract Detected';
                    } else {
                        contractBadge.className = 'not-contract-badge';
                        contractBadge.textContent = '⚠ May not be a contract';
                    }
                    
                    result.style.display = 'block';
                    result.scrollIntoView({ behavior: 'smooth' });
                }
            } catch (err) {
                loading.style.display = 'none';
                error.textContent = '❌ Failed to connect to server. Please try again.';
                error.style.display = 'block';
            }

            btn.disabled = false;
        }
    </script>
</body>
</html>
Updated README.md
Markdown

Copy
# ContractScan 🔍

**AI-powered contract analyzer.** Upload any contract (PDF, DOCX, DOC, TXT) and get instant analysis of key terms, risky clauses, and a plain-English summary.

🚀 **Live Demo:** [https://documind-6kv5kn89t-documind-ai-s-projects.vercel.app](your-url)

---

## ⚡ The Problem

People sign contracts every day without understanding them:
- Employment agreements with hidden non-competes
- Rental leases with unfair penalties  
- Service contracts with auto-renewal traps
- NDAs that are way too broad

**Lawyers cost $300-500/hour.** Most people can't afford that.

---

## ✅ The Solution

ContractScan uses AI to make contract review **free and accessible**:

| Feature | What It Does |
|---------|-------------|
| 📋 **Contract Type Detection** | Identifies what kind of contract it is |
| 👥 **Party Extraction** | Who's involved and their roles |
| 📅 **Key Dates** | Deadlines, start/end dates, milestones |
| 💰 **Financial Terms** | Payments, penalties, fees, hidden costs |
| ⚠️ **Risk Detection** | Flags HIGH/MEDIUM/LOW risk clauses |
| ❓ **Missing Clauses** | Standard protections that should be there |
| 📝 **Plain English Summary** | Explains what you're actually agreeing to |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **AI Engine** | Groq API (Llama 3.1) — **FREE tier** |
| **Document Processing** | PyPDF2, python-docx |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Railway (backend), Vercel (frontend) |

---

## 📊 Example Analysis

**Input:** Employment contract PDF

**Output:**
📋 CONTRACT TYPE Employment Agreement
👥 PARTIES INVOLVED • Employee: John Doe • Employer: TechCorp Inc.
📅 KEY DATES & DEADLINES • Start Date: January 15, 2024 • Review Period: 90 days • Notice Period: 30 days
💰 FINANCIAL TERMS • Salary: $85,000/year • Bonus: Up to 10% based on performance • Health insurance: Employer pays 80%
⚠️ RISKY CLAUSES 🔴 HIGH RISK: Non-compete clause prevents working in same industry for 2 years after leaving 🟡 MEDIUM RISK: Intellectual property assignment is very broad 🟢 LOW RISK: 30-day termination notice is shorter than standard 60 days
❓ MISSING STANDARD CLAUSES • Severance package details • Remote work policy • Expense reimbursement procedure
📝 PLAIN ENGLISH SUMMARY You're agreeing to work for TechCorp for $85k/year. The big red flag is the non-compete — you can't work in tech for 2 years if you leave. Also, they own everything you create, even outside work hours. Consider negotiating these points before signing.
Text

Unwrap

Copy

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/vigneshsai52/contractscan.git
cd contractscan

# Backend setup
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python app.py

# Frontend (open index.html or use live server)
🧠 What I Learned
Challenge	Solution
PDF parsing edge cases	Handled scanned vs text-based PDFs, encoding issues
AI cost management	Used Groq's free tier instead of expensive OpenAI
Structured output	Prompt engineering for consistent analysis format
Multi-format support	Unified text extraction for PDF, DOCX, TXT
CORS deployment	Configured Railway/Vercel for cross-origin requests
