import requests
import json

# Define the FHIR server base URL
base_url = "http://localhost:8080/fhir"

# Patient ID and MedicationRequest ID (replace with actual created IDs)
patient_id = "67"
medication_request_id = "78"
binary_id = "77"

# Function to fetch a specific resource
def fetch_resource(resource_type, resource_id):
    url = f"{base_url}/{resource_type}/{resource_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Successfully fetched {resource_type} with ID {resource_id}")
        return response.json()
    else:
        print(f"Failed to fetch {resource_type} with ID {resource_id}. Status code: {response.status_code}")
        return None

# Fetch the Patient resource
patient_data = fetch_resource("Patient", patient_id)

# Extract and display relevant patient details
if patient_data:
    patient_name = f"{patient_data.get('name', [{}])[0].get('given', ['Not Available'])[0]} {patient_data.get('name', [{}])[0].get('family', 'Not Available')}"
    patient_address = f"{', '.join(patient_data.get('address', [{}])[0].get('line', ['Not Available']))}, {patient_data.get('address', [{}])[0].get('city', 'Not Available')}, {patient_data.get('address', [{}])[0].get('country', 'Not Available')}"
    print(f"Patient Name: {patient_name}")
    print(f"Patient Address: {patient_address}")

# Fetch the MedicationRequest resource
medication_data = fetch_resource("MedicationRequest", medication_request_id)

# Debug: Print the entire MedicationRequest data to inspect its structure
if medication_data:
    print("\nFull MedicationRequest Data:")
    # print(json.dumps(medication_data, indent=4))  # Pretty print the entire JSON

    # Extract and display relevant medication details
    medicines = medication_data.get("medicationCodeableConcept", {}).get("text", "Not Available")
    directions = medication_data.get("dosageInstruction", [{}])[0].get("text", "Not Available")
    refill = medication_data.get("dispenseRequest", {}).get("numberOfRepeatsAllowed", "Not Available")
    
    print(f"Medicines: {medicines}")
    print(f"Directions: {directions}")
    print(f"Refill: {refill}")





def fetch_resource(resource_type, resource_id):
    url = f"{base_url}/{resource_type}/{resource_id}"
    print(f"Fetching resource from: {url}")  # Debugging: print the URL
    response = requests.get(url)
    
    # Log response status code and raw content
    print(f"Response Status Code: {response.status_code}")
    # print(f"Response Content: {response.text[:200]}...")  # Print first 200 chars of response text for inspection

    # Check if response is empty or invalid
    if response.status_code == 200:
        # Check if response seems to be binary (e.g., image)
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except json.JSONDecodeError:
                # print(f"Error: The respon``se for {resource_type} with ID {resource_id} is not valid JSON.")
                # print(f"Response status code: {response.status_code}")
                # print("Raw response content:")
                # print(response.text)  # Print raw response content for inspection
                return None
        elif "image" in response.headers.get("Content-Type", ""):  # Check if the response is an image
            # print("Binary data (image) received.")
            return response.content  # Return binary content (image)
        else:
            # print(f"Unexpected content type: {response.headers.get('Content-Type')}")
            return None
    else:
        print(f"Failed to fetch {resource_type} with ID {resource_id}. Status code: {response.status_code}")
        print("Response content:", response.text)
        return None

# Fetch the Patient resource
patient_data = fetch_resource("Patient", patient_id)

# Extract and display relevant patient details
if patient_data:
    patient_name = f"{patient_data.get('name', [{}])[0].get('given', ['Not Available'])[0]} {patient_data.get('name', [{}])[0].get('family', 'Not Available')}"
    patient_address = f"{', '.join(patient_data.get('address', [{}])[0].get('line', ['Not Available']))}, {patient_data.get('address', [{}])[0].get('city', 'Not Available')}, {patient_data.get('address', [{}])[0].get('country', 'Not Available')}"
    print(f"Patient Name: {patient_name}")
    print(f"Patient Address: {patient_address}")

# Fetch the Binary resource (attachment) for image
binary_data = fetch_resource("Binary", binary_id)

# Save the image if binary data is found
if binary_data:
    print("\nSaving Image Data...")
    
    try:
        # Save the binary data to a file
        file_name = "patient_image.jpg"  # You can change the extension based on image type (e.g., .png, .jpg)
        with open(file_name, 'wb') as f:
            f.write(binary_data)
        print(f"Image saved as {file_name}")
    except Exception as e:
        print(f"Error saving image: {e}")