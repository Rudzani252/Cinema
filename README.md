Cinema Client–Server Application

a Python-based client–server cinema management system. It allows users to register, log in, manage movies, and buy tickets using a Tkinter GUI client and a socket-based server connected to a MySQL database.

Server:
The server listens for incoming client connections using TCP sockets. It receives requests in JSON format and processes them.
setup:
install required libraries:
pip install mysql-connector-python

client:
The client is a Tkinter-based GUI application that allows users to:
Register and log in,
Add, update, and delete movies,
Buy movie tickets,
View movie listings.
The client communicates with the server via JSON socket requests.
Setup:
install required libraries:
pip install mysql-connector-python bcrypt



Authentication System:
User credentials are stored in a SQLite database (users.db).
Passwords are securely hashed using bcrypt.
The login system validates usernames before granting access.

Technical tools and libraries:
Python 3,
socket,
threading,
json,
mysql-connector-python,
Tkinter,
SQLite.

Database:
The program uses MySQL database to store moives that are currently showing and to store the sales records. 
