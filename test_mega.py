from mega import Mega

# Replace with your Mega.nz credentials
MEGA_EMAIL = "niranjanasokan14@gmail.com"
MEGA_PASSWORD = "Niranjan@2004"

mega = Mega()
mega_instance = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

if mega_instance:
    print("✅ Successfully logged into Mega.nz!")
else:
    print("❌ Login failed. Check credentials.")
