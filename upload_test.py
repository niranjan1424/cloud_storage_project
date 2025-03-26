from mega import Mega

# Login to Mega.nz
mega = Mega()
MEGA_EMAIL = "niranjanasokan14@gmail.com"  # Replace with your Mega.nz email
MEGA_PASSWORD = "Niranjan@2004"  # Replace with your Mega.nz password
mega_instance = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

# Upload a test file
file_path = "C:\Users\LENOVO\Documents\Cloud storage\Payment Status.pdf"  # Make sure this file exists in the same folder

# Upload and get the file name
uploaded_file = mega_instance.upload(file_path)
print(f"Uploaded File: {uploaded_file}")
