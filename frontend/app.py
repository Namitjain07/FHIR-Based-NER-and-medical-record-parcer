import streamlit as st
import requests
import time
from pdf2image import convert_from_bytes
import ast
import pandas as pd
from PIL import Image
import io
import os

URL = "http://127.0.0.1:8000/extract_from_doc"

st.set_page_config(page_title="Medical Data Extractor", page_icon="👩‍⚕", layout="wide")
st.title("FHIR Data Submission and Early Prediction via Classification")

# Main input mode selection
input_mode = st.radio("Select Input Mode:", ["Upload a PDF/Image", "Manual Entry", "Radiological Lab", "View Patient Report"], horizontal=True)


def load_data():
    return pd.read_csv('patient_data.csv')

def display_patient_report(data, patient_id, binary_id, report_id):
    # Filter the data based on the input parameters
    patient_data = data[
        (data['Patient_ID'] == int(patient_id)) &
        (data['Binary_ID'] == int(binary_id)) &
        (data['Medical_Report_ID'] == int(report_id))
    ]

    if patient_data.empty:
        st.error("No matching records found.")
        return

    # Display the patient's information
    patient_info = patient_data.iloc[0]  # Get the first matching record
    st.write(f"**Name:** {patient_info['Name']}")
    st.write(f"**Address:** {patient_info['Address']}")
    st.write(f"**Medicines:** {patient_info['Medicines']}")
    st.write(f"**Dosage:** {patient_info['Dosage']}")
    st.write(f"**Refill Information:** {patient_info['Refill']}")
    st.write(f"**Prediction:** {patient_info['Prediction']}")


    # Display the image if it exists in the data
    if 'Image_Column' in patient_info and pd.notna(patient_info['Image_Column']):
        
        try:
            image_path = patient_info['Image_Column']
            
            # Check if the file exists at the given path
            if os.path.exists(image_path):
                # Open and display the image from the file path
                image = Image.open(image_path)
                st.image(image, caption="Patient Image", use_container_width=True)  # Use use_container_width instead of use_column_width
            else:
                st.error(f"Image file not found at path: {image_path}")
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.info("No image available for this patient.")
    
    if 'Predicted' in patient_info and pd.notna(patient_info['Predicted']):
        st.write(f"**Predicted Disease:** {patient_info['Predicted']}")
        


# Panel 1: Upload a PDF/Image
if input_mode == "Upload a PDF/Image":
    file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])
    file_format = st.radio(
        label="Select type of document",
        # options=["prescription", "patient_details"],
        options=["prescription"],
        horizontal=True
    )
    if file and st.button("Extract Data", type="primary"):
        with st.spinner("Extracting data..."):
            bar = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                bar.progress(i)
            payload = {'file_format': file_format}
            files = [('file', (file.name, file.getvalue(), file.type))]
            response = requests.post(URL, data=payload, files=files)
            data = response.json()
            if data:
                st.session_state.extracted_data = data
    if file:
        # Display first page if PDF
        if file.type == "application/pdf":
            pages = convert_from_bytes(file.getvalue(), poppler_path=None)
            st.subheader("Uploaded Document (First Page):")
            st.image(pages[0])
        else:
            st.subheader("Uploaded Image:")
            st.image(file)
        if "extracted_data" in st.session_state:
            st.subheader("Extracted Details")
            
            images_base64 = []
            if "images_base64" in st.session_state.extracted_data:
                images_base64 = st.session_state.extracted_data["images_base64"]
                for idx, image_base64 in enumerate(images_base64):
                    st.subheader(f"Extracted Image {idx + 1}:")
                    st.image(f"data:image/png;base64,{image_base64}")
            # Prescription panel
            if file_format == "prescription":
                name = st.text_input(label="Name", value=st.session_state.extracted_data.get("patient_name", ""))
                address = st.text_input(label="Address", value=st.session_state.extracted_data.get("patient_address", ""))
                medicines = st.text_input(label="Medicines", value=st.session_state.extracted_data.get("medicines", ""))
                directions = st.text_input(label="Directions", value=st.session_state.extracted_data.get("directions", ""))
                refill = st.text_input(label="Refill", value=st.session_state.extracted_data.get("refill", ""))
                if st.button("Submit", type="primary"):
                    final_data = {
                        "type": "prescription",
                        "patient_name": name,
                        "patient_address": address,
                        "medicines": medicines,
                        "directions": directions,
                        "refill": refill,
                        "images_base64": images_base64
                    }
                    
                    
                    # Dynamically create Patient and MedicationRequest FHIR resources
                    patient_id = "1234"  # Unique ID for the patient, could be dynamically generated or fetched from elsewhere

                    # Create the Patient entry
                    patient_entry = {
                        "request": {
                            "method": "POST",
                            "url": "Patient"
                        },
                        "resource": {
                            "resourceType": "Patient",
                            "id": patient_id,
                            "name": [
                                {
                                    "use": "official",
                                    "family": final_data["patient_name"].split(" ")[-1],  # Last name (split by space)
                                    "given": final_data["patient_name"].split(" ")[:-1]  # First name
                                }
                            ],
                            "address": [
                                {
                                    "line": [final_data["patient_address"]],
                                    "city": "Unknown",  # Could be extracted from the address if needed
                                    "country": "Unknown"  # Could be extracted from the address if needed
                                }
                            ]
                        }
                    }

                    # Create Binary Resources for Images
                    binary_entries = []
                    for i, img in enumerate(final_data["images_base64"]):
                        binary_entry = {
                            "request": {
                                "method": "POST",
                                "url": "Binary"
                            },
                            "resource": {
                                "resourceType": "Binary",
                                "id": f"image-{i+1}",
                                "contentType": "image/jpeg",
                                "data": img  # Base64-encoded image data
                            }
                        }
                        binary_entries.append(binary_entry)

                    # Create the MedicationRequest entry
                    medication_request_entry = {
                        "request": {
                            "method": "POST",
                            "url": "MedicationRequest"
                        },
                        "resource": {
                            "resourceType": "MedicationRequest",
                            "status": "active",
                            "intent": "order",
                            "medicationCodeableConcept": {
                                "text": final_data["medicines"]
                            },
                            "subject": {
                                "reference": f"Patient/{patient_id}",
                                "display": final_data["patient_name"]
                            },
                            "reasonCode": [
                                {
                                    "text": final_data["directions"]
                                }
                            ],
                            "dispenseRequest": {
                                "numberOfRepeatsAllowed": 0,
                                "quantity": {
                                    "value": 1,
                                    "unit": "Prescription"
                                },
                                "expectedSupplyDuration": {
                                    "value": 30,
                                    "unit": "days"
                                }
                            },
                            "note": [
                                {
                                    "text": f"Directions: {final_data['directions']}"
                                },
                                {
                                    "text": f"Refill information: {final_data['refill']}"
                                }
                            ],
                            "dosageInstruction": [
                                {
                                    "text": f"Take the prescribed medicines according to the directions provided."
                                }
                            ],
                            "attachment": [
                                {
                                    "contentType": "image/jpeg",
                                    "url": f"Binary/image-{i+1}"
                                } for i in range(len(final_data["images_base64"]))
                            ]
                        }
                    }

                    # Create Bundle
                    bundle = {
                        "resourceType": "Bundle",
                        "type": "transaction",
                        "entry": [patient_entry] + binary_entries + [medication_request_entry]
                    }


                    # Convert bundle to JSON string for sending to the FHIR server
                    import json
                    bundle_json = json.dumps(bundle)


                    st.subheader("Final Submitted Data")
                    st.json(bundle_json)
                    
                    fhir_url = "http://localhost:8080/fhir"  # Assuming the FHIR server is running locally on port 8080
                    headers = {
                        "Content-Type": "application/json"
                    }
                    
                    
                    try:
                        response = requests.post(fhir_url, data=bundle_json, headers=headers)
                        response.raise_for_status()  # Will raise an HTTPError if the response code was not 2xx
                        # If the request is successful
                        # st.success("Details successfully recorded.")
                        st.subheader(f"Response from FHIR server:")
                        st.subheader(f"Status Code: {response.status_code}")
                        st.json(f"{response.text}")
                    except requests.exceptions.RequestException as e:
                        # Handle errors in case of connection issues or invalid responses
                        st.error(f"Error sending data to FHIR server: {e}")
                        
                    
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.success("Details successfully recorded.")
            # # Patient details panel
            # elif file_format == "patient_details":
            #     name = st.text_input(label="Name", value=st.session_state.extracted_data.get("patient_name", ""))
            #     phone = st.text_input(label="Phone No.", value=st.session_state.extracted_data.get("phone_no", ""))
            #     vacc_status = st.text_input(label="Hepatitis B vaccination status", value=st.session_state.extracted_data.get("vaccination_status", ""))
            #     med_problems = st.text_input(label="Medical Problems", value=st.session_state.extracted_data.get("medical_problems", ""))
            #     has_insurance = st.text_input(label="Has Insurance?", value=st.session_state.extracted_data.get("has_insurance", ""))
            #     if st.button("Submit", type="primary"):
            #         final_data = {
            #             "type": "patient_details",
            #             "patient_name": name,
            #             "phone_no": phone,
            #             "vaccination_status": vacc_status,
            #             "medical_problems": med_problems,
            #             "has_insurance": has_insurance,
            #             "images_base64": images_base64
            #         }
            #         st.subheader("Final Submitted Data")
            #         st.json(final_data)
            #         for key in list(st.session_state.keys()):
            #             del st.session_state[key]
            #         st.success("Details successfully recorded.")

# Panel 2: Manual Entry
elif input_mode == "Manual Entry":
    st.subheader("Enter the Details Manually")
    doc_type = st.radio("Select type of document",
                        # ["prescription", "patient_details"],
                        ["prescription"],

                        horizontal=True)
    if doc_type == "prescription":
        name = st.text_input("Patient Name")
        address = st.text_input("Address")
        medicines = st.text_area("Medicines")
        directions = st.text_area("Directions")
        refill = st.text_input("Refill")
    else:
        name = st.text_input("Patient Name")
        phone = st.text_input("Phone No.")
        vacc_status = st.text_input("Hepatitis B Vaccination Status")
        med_problems = st.text_area("Medical Problems")
        has_insurance = st.text_input("Has Insurance? (Yes/No)")
    if st.button("Submit Data", type="primary"):
        if doc_type == "prescription":
            final_data = {
                "type": "prescription",
                "patient_name": name,
                "patient_address": address,
                "medicines": medicines,
                "directions": directions,
                "refill": refill
            }
        else:
            final_data = {
                "type": "patient_details",
                "patient_name": name,
                "phone_no": phone,
                "vaccination_status": vacc_status,
                "medical_problems": med_problems,
                "has_insurance": has_insurance
            }
        st.subheader("Final Submitted Data")
        st.json(final_data)
        st.success("Details successfully recorded.")
        
        

# Panel 3: Radiological Lab
elif input_mode == "Radiological Lab":
    st.subheader("Enter Radiological Lab Details")
    # test_name = st.text_input("Test Name")
    # patient_name = st.text_input("Patient Name")
    # radiologist_name = st.text_input("Radiologist Name")
    # test_date = st.date_input("Test Date")
    # findings = st.text_area("Findings")
    # recommendations = st.text_area("Recommendations")
    # scan_report = st.selectbox("Select Scan Report Type", ["MRI", "CT", "X-Ray", "Ultrasound", "Other"])
    patient_id = st.text_input("Patient ID")
    image_file = st.file_uploader("Upload Test Image (optional)", type=["png", "jpg", "jpeg"])

    if image_file:
        st.subheader("Uploaded Image:")
        st.image(image_file)

    if st.button("Submit Radiology Data", type="primary"):
        # radiology_data = {
        #     "test_name": test_name,
        #     "patient_name": patient_name,
        #     "radiologist_name": radiologist_name,
        #     "test_date": test_date.isoformat(),
        #     "findings": findings,
        #     "recommendations": recommendations,
        #     "scan_report": scan_report
        # }
        # if image_file:
            # radiology_data["image_name"] = image_file.name
        st.subheader("Final Radiology Data")
        # st.json(radiology_data)
        st.success("Radiology details successfully recorded.")








elif input_mode == "View Patient Report":
    data = load_data()
    st.subheader("Enter Patient Query")

    patient_id = st.text_input("Patient ID")
    binary_id = st.text_input("Binary ID")
    report_id = st.text_input("Medical Report ID")

    if st.button("Fetch Report"):
        if patient_id and binary_id and report_id:
            display_patient_report(data, patient_id, binary_id, report_id)
        else:
            st.warning("Please fill in all the fields.")


