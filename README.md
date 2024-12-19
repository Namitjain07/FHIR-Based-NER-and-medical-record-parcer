# Smart Healthcare: Prescription Parsing and Cancer Detection

# Overview
This project is an Smart healthcare system designed to:

- Read and Extract Prescription Data using OCR (Pytesseract).
- Convert Prescription Data to JSON Format for seamless integration with an FHIR server.
- Analyze Skin Cancer Images to determine if a lesion is Malignant or Benign using deep learning.
- Integrate patient reports, showcasing their prescriptions and skin analysis results to assist healthcare providers in determining the need for treatment.

-----------------------------------------------------------------------------
<h2>OCR-Based Prescription Analysis</h2>

- Reads printed prescriptions using Pytesseract and Optical Character Recognition (OCR).
- Extracts relevant data (e.g., medication names, dosages, instructions) and converts it into JSON format.
- Uploads prescription data to an FHIR server for storage and further processing.

----------------------------------------------------------------------------
<h2>Skin Cancer Detection</h2>

- Utilizes EfficientNet and EfficientNetB3 models to analyze skin images and classify them as Malignant or Benign.
- Provides fast and reliable predictions to assist in early diagnosis and treatment planning.

----------------------------------------------------------------------------
<h2>Patient Report Integration</h2>

- Combines prescription data and skin analysis results into a single patient report.
- Displays medication details and cancer detection outcomes in a user-friendly interface.
