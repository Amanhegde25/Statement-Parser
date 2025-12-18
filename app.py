from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import io
import sys
from src.components.parser import LocalAIParser
from src.logger import logging
from src.exception import CustomException

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            model_name = request.form.get('model_name', 'llama3.2:1b')
            files = request.files.getlist('files')
            
            if not files or files[0].filename == '':
                logging.warning("POST request received but no files were selected.")
                return "No files selected", 400

            logging.info(f"Starting batch processing for {len(files)} files using model: {model_name}")
            
            parser = LocalAIParser(model_name=model_name)
            results = []

            for file in files:
                logging.info(f"Received file: {file.filename}")
                
                # Save file temporarily
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                try:
                    # Parse using the LocalAIParser logic
                    logging.info(f"Forwarding {file.filename} to LocalAIParser.")
                    data = parser.parse(file_path)
                    data["filename"] = file.filename
                    results.append(data)
                except Exception as e:
                    logging.error(f"Failed to parse {file.filename}: {str(e)}")
                    # Continue processing other files even if one fails
                    results.append({"filename": file.filename, "error": "Processing failed"})
                finally:
                    # Always cleanup the file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.info(f"Temporary file removed: {file_path}")

            # Data Transformation
            logging.info("Generating DataFrame and formatting results.")
            df = pd.DataFrame(results)
            
            preferred_order = ["filename", "issuer", "total_balance", "due_date", "statement_date", "account_last_4"]
            # Filter columns that actually exist in the result
            existing_cols = [c for c in preferred_order if c in df.columns]
            other_cols = [c for c in df.columns if c not in preferred_order]
            final_df = df[existing_cols + other_cols]

            logging.info("Batch processing complete. Rendering results table.")
            
            return render_template('index.html', 
                                    tables=[final_df.to_html(classes='table table-striped', header="true", index=False)], 
                                    csv_data=final_df.to_csv(index=False),
                                    model_name=model_name)

        return render_template('index.html')

    except Exception as e:
        logging.error(f"Unexpected error in web route: {str(e)}")
        raise CustomException(e, sys)

@app.route('/download', methods=['POST'])
def download():
    try:
        csv_content = request.form.get('csv_content')
        if not csv_content:
            logging.error("Download requested but no CSV content found in form data.")
            return "No data to download", 400
            
        logging.info("Generating CSV file for user download.")
        proxy = io.StringIO(csv_content)
        mem = io.BytesIO()
        mem.write(proxy.getvalue().encode('utf-8'))
        mem.seek(0)
        
        return send_file(
            mem, 
            mimetype='text/csv', 
            as_attachment=True, 
            download_name="parsed_statements.csv"
        )
    except Exception as e:
        logging.error(f"Error during file download: {str(e)}")
        raise CustomException(e, sys)

if __name__ == '__main__':
    logging.info("Flask Server started on http://127.0.0.1:5000")
    app.run(debug=True)