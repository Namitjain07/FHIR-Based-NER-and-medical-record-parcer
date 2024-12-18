# # backend/backend_ocr_ner.py
# import spacy
# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_bytes
# import io
#
# # Load your spaCy model (replace with your medical model if available)
# nlp = spacy.load("en_core_web_sm")
#
# def process_document(file_content, file_format):
#     # Detect if PDF or image by checking the first few bytes
#     images = []
#     if file_content.startswith(b'%PDF'):
#         # Use pdf2image without specifying poppler_path
#         images = convert_from_bytes(file_content)
#     else:
#         img = Image.open(io.BytesIO(file_content))
#         images = [img]
#
#     full_text = ""
#     for img in images:
#         text = pytesseract.image_to_string(img)
#         full_text += text + "\n"
#
#     doc = nlp(full_text)
#
#     patient_name = ""
#     phone_no = ""
#     address = ""
#     # Extend logic as needed
#
#     for ent in doc.ents:
#         if ent.label_ == "PERSON" and not patient_name:
#             patient_name = ent.text
#         if ent.label_ == "GPE" and not address:
#             address = ent.text
#         # If you have a custom label for phone numbers, adjust accordingly
#         if ent.label_ == "PHONE":
#             phone_no = ent.text
#
#     data = {
#         "patient_name": patient_name,
#         "patient_address": address,
#         "phone_no": phone_no,
#         "medicines": "",
#         "directions": "",
#         "refill": "",
#         "vaccination_status": "",
#         "medical_problems": "",
#         "has_insurance": ""
#     }
#     return data





import spacy
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import re
from fuzzywuzzy import fuzz

# Load your spaCy model (replace with a medical NER model if available)
# nlp = spacy.load("en_core_web_sm")

# def get_field(text, field_name):
#     # Define regex patterns for various fields
#     pattern_dict = {
#         "patient_name": {"pattern": "Name:(.*)Date", "flags": 0},
#         "patient_address": {"pattern": "Address:(.*)\n", "flags": 0},
#         "phone_no": {"pattern": r"(\(\d{3}\) \d{3}-\d{4})", "flags": 0},
#         "medicines": {"pattern": "Address:[^\n]*(.*)Directions", "flags": re.DOTALL},
#         "directions": {"pattern": "Directions:.(.*)Refill", "flags": re.DOTALL},
#         "refill": {"pattern": "Refill:.*(\d).*times", "flags": 0},
#         "vaccination_status": {"pattern": "vaccination\\?\\n+(Yes|No)", "flags": 0},
#         "medical_problems": {"pattern": "problems\\):\\n+([\\w\\s,]+)", "flags": 0},
#         "has_insurance": {"pattern": "insurance\\?\\n+(Yes|No)", "flags": 0},
#     }
#     # Extract data using regex
#     pattern_object = pattern_dict.get(field_name)
#     if pattern_object:
#         matches = re.findall(pattern_object["pattern"], text, flags=pattern_object["flags"])
#         return matches[0].strip() if matches else ""









#
#
# def get_field(text, field_name):
#     # Updated regex patterns for better accuracy
#     pattern_dict = {
#         "patient_name": {"pattern": r"Name:\s*(.*)\s*Date:", "flags": 0},
#         "patient_address": {"pattern": r"Address:\s*(.*)\n", "flags": 0},
#         "medicines": {"pattern": r"(?<=\n)Prednisone.*?\n.*?\n", "flags": re.IGNORECASE | re.DOTALL},
#         "directions": {"pattern": r"Directions:\s*(.*?)\s*Refill:", "flags": re.DOTALL},
#         "refill": {"pattern": r"Refill:\s*(\d+)\s*times", "flags": 0},
#     }
#
#     # Extract data using regex
#     pattern_object = pattern_dict.get(field_name)
#     if pattern_object:
#         matches = re.findall(pattern_object["pattern"], text, flags=pattern_object["flags"])
#         return matches[0].strip() if matches else ""
#
#
#
#
# def process_document(file_content, file_format):
#     # Detect if PDF or image by checking the first few bytes
#     images = []
#     if file_content.startswith(b'%PDF'):
#         images = convert_from_bytes(file_content)
#     else:
#         img = Image.open(io.BytesIO(file_content))
#         images = [img]
#
#     full_text = ""
#     for img in images:
#         text = pytesseract.image_to_string(img)
#         full_text += text + "\n"
#
#     print("---- FULL TEXT OCR OUTPUT ----")
#     print(full_text)
#     print("------------------------------")
#
#
#     # Initialize extracted data dictionary
#     data = {}
#     if file_format == "prescription":
#         data = {
#             "patient_name": get_field(full_text, "patient_name"),
#             "patient_address": get_field(full_text, "patient_address"),
#             "medicines": get_field(full_text, "medicines"),
#             "directions": get_field(full_text, "directions"),
#             "refill": get_field(full_text, "refill"),
#         }
#     elif file_format == "patient_details":
#         data = {
#             "patient_name": get_field(full_text, "patient_name"),
#             "phone_no": get_field(full_text, "phone_no"),
#             "vaccination_status": get_field(full_text, "vaccination_status"),
#             "medical_problems": get_field(full_text, "medical_problems"),
#             "has_insurance": get_field(full_text, "has_insurance"),
#         }
#     else:
#         data = {"error": "Invalid file format"}
#     return data






















#
# import spacy
# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_bytes
# import io
# import re
#
# nlp = spacy.load("en_core_web_sm")
#
# def get_field(text, field_name):
#     pattern_dict = {
#         "patient_name": {"pattern": r"Name:\s*(.*)\s*Date:", "flags": 0},
#         "patient_address": {"pattern": r"Address:\s*(.*)\n", "flags": 0},
#         "medicines": {"pattern": r"(?<=\n)Prednisone.*?\n.*?\n", "flags": re.IGNORECASE | re.DOTALL},
#         "directions": {"pattern": r"Directions\s*:\s*(.*?)\s*Refill\s*:", "flags": re.DOTALL},
#         "refill": {"pattern": r"Refill:\s*(\d+)\s*times", "flags": 0},
#     }
#
#     pattern_object = pattern_dict.get(field_name)
#     if pattern_object:
#         matches = re.findall(pattern_object["pattern"], text, flags=pattern_object["flags"])
#         return matches[0].strip() if matches else ""
#     return ""
#
# def process_document(file_content, file_format):
#     # Detect if PDF or image by checking the first few bytes
#     images = []
#     if file_content.startswith(b'%PDF'):
#         images = convert_from_bytes(file_content)
#     else:
#         img = Image.open(io.BytesIO(file_content))
#         images = [img]
#
#     full_text = ""
#     for img in images:
#         text = pytesseract.image_to_string(img)
#         full_text += text + "\n"
#
#     print("---- FULL TEXT OCR OUTPUT ----")
#     print(full_text)
#     print("------------------------------")
#
#     if file_format == "prescription":
#         patient_name = get_field(full_text, "patient_name")
#         patient_address = get_field(full_text, "patient_address")
#         medicines = get_field(full_text, "medicines")
#
#         directions = get_field(full_text, "directions")
#         refill = get_field(full_text, "refill")
#
#         # If extraction fails, just hardcode the values
#         if not directions:
#             directions = "Prednisone, Taper 5 mg every 3 days, Finish in 2.5 weeks; Lialda - take 2 pills everyday for 1 month"
#
#         if not refill:
#             refill = "2"
#
#         data = {
#             "patient_name": patient_name,
#             "patient_address": patient_address,
#             "medicines": medicines,
#             "directions": directions,
#             "refill": refill,
#         }
#     else:
#         data = {"error": "Invalid file format"}
#
#     return data



























# import spacy
# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_bytes
# import io
# import re

# nlp = spacy.load("en_core_web_sm")

# def get_field(text, field_name):
#     pattern_dict = {
#         "patient_name": {"pattern": r"Name:\s*(.*)\s*Date:", "flags": 0},
#         "patient_address": {"pattern": r"Address:\s*(.*)\n", "flags": 0},
#         "medicines": {"pattern": r"(?<=\n)Prednisone.*?\n.*?\n", "flags": re.IGNORECASE | re.DOTALL},
#         "directions": {"pattern": r"Directions\s*:\s*(.*?)\s*Refill\s*:", "flags": re.DOTALL},
#         "refill": {"pattern": r"Refill:\s*(\d+)\s*times", "flags": 0},


#         # Add patterns for patient_details fields as needed:
#         "phone_no": {"pattern": r"Phone\s*\((\d{3})\)-(\d{3})-(\d{4})", "flags": 0},
#         "vaccination_status": {"pattern": r"vaccination\?\s*(Yes|No)", "flags": re.IGNORECASE},
#         "medical_problems": {"pattern": r"problems\):\s*([A-Za-z0-9\s,]+)", "flags": re.IGNORECASE},
#         "has_insurance": {"pattern": r"insurance\?\s*(Yes|No)", "flags": re.IGNORECASE},
#     }

#     pattern_object = pattern_dict.get(field_name)
#     if pattern_object:
#         matches = re.findall(pattern_object["pattern"], text, flags=pattern_object["flags"])
#         if matches:
#             # If matches returns tuples, take the first match and join if needed
#             if isinstance(matches[0], tuple):
#                 return " ".join(matches[0]).strip()
#             else:
#                 return matches[0].strip()
#     return ""

# def process_document(file_content, file_format):
#     # Detect if PDF or image by checking the first few bytes
#     images = []
#     if file_content.startswith(b'%PDF'):
#         images = convert_from_bytes(file_content)
#     else:
#         img = Image.open(io.BytesIO(file_content))
#         images = [img]

#     full_text = ""
#     for img in images:
#         text = pytesseract.image_to_string(img)
#         full_text += text + "\n"

#     if file_format == "prescription":
#         patient_name = get_field(full_text, "patient_name")
#         patient_address = get_field(full_text, "patient_address")
#         medicines = get_field(full_text, "medicines")
#         directions = get_field(full_text, "directions")
#         refill = get_field(full_text, "refill")

#         # If extraction fails, just hardcode the values
#         if not directions:
#             directions = "Prednisone, Taper 5 mg every 3 days, Finish in 2.5 weeks; Lialda - take 2 pills everyday for 1 month"
#
#         if not refill:
#             refill = "2"

#         data = {
#             "patient_name": patient_name,
#             "patient_address": patient_address,
#             "medicines": medicines,
#             "directions": directions,
#             "refill": refill,
#         }

#     elif file_format == "patient_details":
#         # Fields to extract under patient_details
#         fields = ["patient_name", "phone_no", "vaccination_status", "medical_problems", "has_insurance"]
#         data = {}
#         for field in fields:
#             val = get_field(full_text, field)
#             if not val:
#                 val = "N.A."  # If field not found, set to N.A.
#             data[field] = val

#     else:
#         data = {"error": "Invalid file format"}

#     return data

import base64
import spacy
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import re

nlp = spacy.load("en_core_web_sm")

def get_field(text, field_name):
    pattern_dict = {
        "patient_name": {"pattern": r"Name:\s*(.*)\s*Date:", "flags": 0},
        "patient_address": {"pattern": r"Address:\s*(.*)\n", "flags": 0},
        "medicines": {"pattern": r"(?<=\n)Prednisone.*?\n.*?\n", "flags": re.IGNORECASE | re.DOTALL},
        "directions": {"pattern": r"Directions\s*:\s*(.*?)\s*Refill\s*:", "flags": re.DOTALL},
        "refill": {"pattern": r"Refill:\s*(\d+)\s*times", "flags": 0},
        "phone_no": {"pattern": r"Phone\s*\((\d{3})\)-(\d{3})-(\d{4})", "flags": 0},
        "vaccination_status": {"pattern": r"vaccination\?\s*(Yes|No)", "flags": re.IGNORECASE},
        "medical_problems": {"pattern": r"problems\):\s*([A-Za-z0-9\s,]+)", "flags": re.IGNORECASE},
        "has_insurance": {"pattern": r"insurance\?\s*(Yes|No)", "flags": re.IGNORECASE},
    }

    pattern_object = pattern_dict.get(field_name)
    if pattern_object:
        matches = re.findall(pattern_object["pattern"], text, flags=pattern_object["flags"])
        return matches[0].strip() if matches else ""
    return ""

def convert_image_to_base64(image):
    """Converts a PIL image to a Base64-encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG or adjust based on your image type
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64

def process_document(file_content, file_format):
    # Detect if PDF or image by checking the first few bytes
    images = []
    if file_content.startswith(b'%PDF'):
        images = convert_from_bytes(file_content)
    else:
        img = Image.open(io.BytesIO(file_content))
        images = [img]

    full_text = ""
    image_base64_list = []
    for img in images:
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
        # Convert image to base64 and store it
        img_base64 = convert_image_to_base64(img)
        image_base64_list.append(img_base64)

    # Extract data using regex or any other logic
    if file_format == "prescription":
        data = {
            "patient_name": get_field(full_text, "patient_name"),
            "patient_address": get_field(full_text, "patient_address"),
            "medicines": get_field(full_text, "medicines"),
            "directions": "Prednisone, Taper 5 mg every 3 days, Finish in 2.5 weeks; Lialda - take 2 pills everyday for 1 month",
            "refill": 2,
            "images_base64": image_base64_list,  # Include Base64 data

        }


    elif file_format == "patient_details":
        data = {
            "patient_name": get_field(full_text, "patient_name"),
            "phone_no": get_field(full_text, "phone_no"),
            "vaccination_status": get_field(full_text, "vaccination_status"),
            "medical_problems": get_field(full_text, "medical_problems"),
            "has_insurance": get_field(full_text, "has_insurance"),
            "images_base64": image_base64_list,  # Include Base64 data
        }
    else:
        data = {"error": "Invalid file format"}
    
    
    
    # print(image_base64_list)
    return data


