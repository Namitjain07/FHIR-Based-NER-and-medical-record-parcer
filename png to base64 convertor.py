import base64
import json

# Read the binary data from a file (e.g., an image)
with open('20230808.jpg', 'rb') as binary_file:
    binary_data = binary_file.read()

# Encode the binary data to a Base64 string
base64_data = base64.b64encode(binary_data).decode('utf-8')

# Create a dictionary to store the Base64 data
data = {
    'data': base64_data
}

# Save the Base64 data to a JSON file
with open('image_data.json', 'w') as json_file:
    json.dump(data, json_file)

print("Image has been successfully encoded and saved as 'image_data.json'")
