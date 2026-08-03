# AI Persona Summarizer 

An intelligent, aesthetically-pleasing web application that not only summarizes your text and web articles but customizes the summary based on **who you are** (Researcher, Student, Teacher, or Child). Powered by LexRank for extractive summarization, YAKE for keyword extraction, and Google's Gemini for persona-based adaptation.

## ✨ Features

- Multi-Source Input:Paste raw text, drop a URL (auto-scraped), or upload a PDF.
- Persona-Based Summarization:Adapt complex text into tones that fit your need.
    - 🔬 *Researcher* (Technical & precise)
    - 📚 *Student* (Exam-ready concepts)
    - 🎓 *Teacher* (Structured & clear)
    - 🌟 *Child* (Simple & friendly)
- **Keyword Extraction & Highlighting:** Automatically identifies the most important concepts and highlights them intelligently in the final summary.
- **Instant Translation:** Translate your generated summary into 20+ languages instantly.
- **Stunning UI/UX:** A fully custom, dark-mode glassmorphism frontend with sleek micro-animations and staggered loading states.

##  Architecture

The application is fully decoupled, consisting of:
1. **Backend API (`server.py`): A lightweight Flask server that orchestrates the heavy lifting—web scraping, text preprocessing, NLP summarization, keyword extraction, and generative AI persona rewriting.
2. **Frontend (`frontend/`): A pure HTML/CSS/JS presentation layer. No bloated frameworks; just clean, animated Vanilla web technologies that fetch data asynchronously from the API.

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Millee-24/AI-text-Summarizer.git
cd AI-text-Summarizer
```

### 2. Set up the Environment
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

*Note: The NLP summarizer (`sumy`) uses `nltk`. You may need to download the `punkt` tokenizer:*
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 3. Add your Gemini API Key
Set your Google Gemini API key as an environment variable:
```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Mac/Linux
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Backend API
Start the Flask server:
```bash
python server.py
```
*The API will start running on `http://localhost:5000`.*

### 5. Launch the Frontend
Because it is a pure HTML/JS frontend, you can simply serve the `frontend/` folder, or just double-click `index.html`!
```bash
cd frontend
python -m http.server 8000
```
Visit `http://localhost:8000` in your browser to experience the app.

---
Built with ❤️ utilizing LexRank, YAKE, and Google Gemini.
