## Statement Parser
A robust, AI-powered tool that extracts key financial data from unstructured credit card statements (PDFs).
Unlike traditional parsers that rely on brittle Regex rules or expensive cloud APIs, this project uses Local Large Language Models (LLMs) to process sensitive financial data entirely offline. No data ever leaves your machine.

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

# File Structure 
    ML_Project/
    ├── logs/
    ├── artifacts/
    ├── notebook/
    ├── src/
    ├── templates/
    ├── .gitignore
    ├── README.md
    ├── app.py
    ├── main.py
    ├── requirements.txt
    ├── setup.py

## Directory & File Explanations

### logs/
* all the logs are created here for checking the progress of the code and trobolshooting

### src/
* Contains the core source code of the project.
* Common sub-components might be:
* * Data loading & preprocessing functions
* * Model training & evaluation scripts
* * Utility modules
* * Purpose: Houses reusable and production-ready code for ML pipelines.

### templates/
* Likely contains template files used by the app (if there’s a web interface) such as:
* * HTML templates
* * UI components
* Purpose: Used for rendering front-end pages if the project includes a web app/visualization interface.

### app.py
* A Python script — likely the entry point for running the application.
* Typical roles might be:
* Serving a model via an API (Flask, FastAPI, etc.)
* Running a training/testing pipeline
* Connecting UI templates with backend logic

### requirements.txt
* Lists the Python packages/dependencies needed for the project.
* Purpose: Allows others to install all required libraries in one step (e.g., pip install -r requirements.txt).

### setup.py
* A Python setup script that can make the project installable as a package.
* Purpose:
* * Defines metadata, dependencies, and packaging details.
* * Enables pip install -r . for editable installs during development.

