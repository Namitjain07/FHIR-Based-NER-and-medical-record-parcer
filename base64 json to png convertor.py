import base64
import json

# Load the JSON file containing the Base64-encoded image data
with open('image_data.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the Base64 data from the JSON object
# Assuming the JSON structure is like {"data": "base64_encoded_string"}
base64_data = data['data']

# Decode the Base64 string into binary data
binary_data = base64.b64decode(base64_data)

# Save the binary data to a new file (e.g., image.jpg)
with open('output_image.jpg', 'wb') as binary_file:
    binary_file.write(binary_data)

print("Image has been successfully decoded and saved as 'output_image.jpg'")
