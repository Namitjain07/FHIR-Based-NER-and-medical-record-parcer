# backend/main_api.py
from fastapi import FastAPI, File, Form, UploadFile
from backend_ocr_ner import process_document
import uvicorn

app = FastAPI()

@app.post("/extract_from_doc")
async def extract_from_doc(file: UploadFile = File(...), file_format: str = Form(...)):
    file_content = await file.read()
    result = process_document(file_content, file_format)
    print(result)
    return result
      # Check the data structure returned


if __name__ == "__main__":
    uvicorn.run("main_api:app", host="127.0.0.1", port=8000, reload=True)
