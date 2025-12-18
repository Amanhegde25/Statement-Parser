import pdfplumber
import requests
import json
import sys
import os
from src.logger import logging
from src.exception import CustomException 

class LocalAIParser:
    def __init__(self, model_name="llama3.2:1b"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        logging.info(f"Initialized LocalAIParser with model: {self.model_name}")

    def extract_text(self, pdf_path):
        text = ""
        try:
            logging.info(f"Opening PDF file for text extraction: {pdf_path}")
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                logging.info(f"PDF opened successfully. Total pages: {num_pages}")
                if num_pages > 0:
                    text += pdf.pages[0].extract_text() or ""
                if len(text) < 100 and num_pages > 1:
                    logging.info("First page text insufficient (<100 chars), extracting second page...")
                    text += pdf.pages[1].extract_text() or ""
            
            logging.info(f"Extraction complete. Total characters extracted: {len(text)}")
        except Exception as e:
            logging.error(f"Error occurred during PDF text extraction: {str(e)}")
            raise CustomException(e, sys)
        return text

    def parse(self, pdf_path):
        try:
            raw_text = self.extract_text(pdf_path)
            if not raw_text.strip():
                logging.warning(f"No text found in {pdf_path}. Possible scanned image or empty file.")
                return {"error": "Empty text. File might be an image."}
            
            prompt = f"""
            You are a highly accurate financial data extraction engine. 
            Analyze the bank statement text provided and extract the following information into a strict JSON format.

            INSTRUCTIONS:
            1. ISSUER: Look for the bank name or financial institution at the top.
            2. ACCOUNT_LAST_4: Extract only the final 4 digits of the credit card or account number.
            3. DATES: Convert all dates to YYYY-MM-DD format.
            4. NUMBERS: Remove currency symbols ($, £, €) and commas. Ensure they are valid floats.
            5. NULLS: If a field is not found, return null.
            6. IFSC_CODE: unique code used by banks in India.

            RETURN ONLY A JSON OBJECT WITH THESE KEYS:
            - "issuer": The exact name of the bank or provider as written in the text.
            - "IFSC_code": The IFSC code if available, else null.
            - "account_last_4": String of 4 digits.
            - "statement_date": YYYY-MM-DD.
            - "due_date": YYYY-MM-DD.
            - "total_balance": Numeric (e.g., 1250.75).
            - "minimum_payment": Numeric (e.g., 35.00).
            - "currency": The 3-letter currency code (e.g., USD, GBP, INR).

            TEXT TO ANALYZE:
            {raw_text[:2500]}
            """

            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.1, 
                    "seed": 42
                }
            }

            logging.info(f"Sending request to Local AI API ({self.model_name})...")
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logging.info("API response received successfully.")
            
            data = json.loads(result['response'])
            
            # Post-processing validation for Issuer
            issuer = data.get('issuer', 'Unknown')
            if issuer and issuer not in raw_text:
                if "Bank" not in issuer and "Card" not in issuer: 
                    logging.warning(f"Extracted issuer '{issuer}' not found in raw text. Flagging as guess.")
                    data['issuer'] = "Not Found in Text (AI Guess)"
            
            logging.info(f"Successfully parsed data for {pdf_path}")
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Ollama API connection error: {str(e)}")
            raise CustomException(e, sys)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON from AI response: {str(e)}")
            raise CustomException(e, sys)
        except Exception as e:
            logging.error(f"Unexpected error in parse method: {str(e)}")
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    TEST_PDF = "eg_input\\391657900-SBI-statement-sample.pdf"  
    MODEL = "llama3.2:1b"    
    logging.info("Running LocalAIParser Standalone Test")
    try:
        # 1. Initialize Parser
        parser = LocalAIParser(model_name=MODEL)
        
        # 2. Check if test file exists
        if not os.path.exists(TEST_PDF):
            logging.error(f"Test file not found: {TEST_PDF}. Please place a PDF in the root directory.")
            print(f"Error: Put a PDF named '{TEST_PDF}' in this folder to test.")
        else:
            # 3. Perform Parsing
            print(f"Processing {TEST_PDF}...")
            result = parser.parse(TEST_PDF)
            
            # 4. Print results to console
            print("\n" + "="*30)
            print("EXTRACTION RESULTS:")
            print("="*30)
            print(json.dumps(result, indent=4))
            print("="*30)
            
    except Exception as e:
        logging.error(f"Main execution block failed: {str(e)}")
        print(f"An error occurred: {e}")