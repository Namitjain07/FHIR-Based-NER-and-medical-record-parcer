import streamlit as st
import pandas as pd

# Function to load the existing CSV file
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty DataFrame with required columns
        return pd.DataFrame(columns=[
            'Patient_ID', 'Binary_ID', 'Medical_Report_ID', 'Name', 'Address', 'Medicines', 'Dosage', 'Refill', 'Image_Column'
        ])

# Function to save the updated data back to the CSV file
def save_csv(data, file_path):
    data.to_csv(file_path, index=False)

# Streamlit app
st.title("Add Patient Parameters to CSV")

# File path for the CSV file
csv_file_path = 'patient_data.csv'

data = load_csv(csv_file_path)

st.subheader("Enter New Patient Data")

# Input fields for the new patient data
patient_id = st.text_input("Patient ID")
binary_id = st.text_input("Binary ID")
medical_report_id = st.text_input("Medical Report ID")
name = st.text_input("Name")
address = st.text_input("Address")
medicines = st.text_input("Medicines")
dosage = st.text_input("Dosage")
refill = st.text_input("Refill Information")
prediction = st.text_input("Prediction")
image_column = st.text_area("Image Data (optional, as string or bytes)")

if st.button("Add to CSV"):
    if patient_id and binary_id and medical_report_id and name and address and medicines and dosage and refill:
        # Add the new data as a row to the DataFrame
        new_row = {
            'Patient_ID': patient_id,
            'Binary_ID': binary_id,
            'Medical_Report_ID': medical_report_id,
            'Name': name,
            'Address': address,
            'Medicines': medicines,
            'Dosage': dosage,
            'Refill': refill,
            'Prediction': prediction,
            'Image_Column': image_column
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        save_csv(data, csv_file_path)

        st.success("New patient data added successfully!")
    else:
        st.error("Please fill in all required fields.")

# Display the updated data
st.subheader("Current Patient Data")
st.dataframe(data)
