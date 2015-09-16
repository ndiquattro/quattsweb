import os
# Set servername for subdomains
if os.uname()[0] == 'Darwin':
    SERVER_NAME = 'localhost:5000'
else:
    SERVER_NAME = 'quatts.net'
