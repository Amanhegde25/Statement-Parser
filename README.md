## Statement Parser

## Tech Stack
* **Frontend:** [Flask](Python)
* **AI Engine:** [Ollama](https://ollama.com/) (running `llama3.2:1b`)
* **PDF Processing:** `pdfplumber` (Layout-preserving text extraction)
* **Language:** Python 3.10+

## Installation & Setup

### 1. Install Prerequisites
You need **Python** installed. You also need **Ollama** to run the AI model.

* Download Ollama: [ollama.com](https://ollama.com)
* put in your environment variables:
    C:\Users\<username>\AppData\Local\Programs\Ollama
* Pull the lightweight model (Run this in your terminal):
    ollama pull llama3.2:1b

### to install requirements
    pip install -r requirements.txt

### To run app file
    python app.py
* app will run in http://localhost:5000/

### To test every file individully 
    python -m <file path>
    eg python -m src.logging


