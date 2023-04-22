import random

# Function to generate and return a random OTP
def generate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp

# Function to send the OTP to the user
def send_otp(user, otp):
    print("OTP sent to", user, ":", otp)

# Function to verify the OTP entered by the user
def verify_otp(user, otp, users):
    if user in users:
        if otp == generate_otp():
            return True
        else:
            return False
    else:
        return False

# Function to login the user
def login():
    # Read user information from file
    with open("users.txt") as f:
        users = {}
        for line in f:
            username, password = line.strip().split(":")
            users[username] = password
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Check if username and password are valid
    if username in users and users[username] == password:
        otp = generate_otp()
        send_otp(username, otp)
        user_otp = input("Enter OTP: ")
        
        # Check if OTP is valid
        if verify_otp(username, user_otp, users):
            print("Login successful!")
        else:
            print("Invalid OTP. Login failed.")
    else:
        print("Invalid username or password. Login failed.")

# Call login function to start the process
login()
