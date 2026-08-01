Cinema Client–Server Application

A Python-based client–server cinema management system that enables users to register, log in, browse currently showing movies, purchase movie tickets, and manage movie records through a Tkinter graphical user interface. The application uses TCP sockets and JSON for client-server communication, with a MySQL database for movie and sales data and SQLite for user authentication.

#Features:
- User registration and login
- Secure password hashing using bcrypt
- Browse currently showing movies
- Purchase movie tickets
- Add, update, and delete movie records
- Client-server communication using TCP sockets
- JSON-based request and response handling
- MySQL database integration for movies and sales records
- 
#Architecture:
Tkinter Client
-
TCP Socket + JSON
-
Python Server
-
MySQL Database

#Server:
The server listens for incoming TCP socket connections from clients. It processes JSON requests, performs the required database operations, and returns responses to the client.
Responsibilities:
- Accept client connections
- Process JSON requests
- Manage movie records
- Process ticket purchases
- Communicate with the MySQL database

#Client:
The client is a Tkinter-based graphical application that allows users to interact with the cinema management system.
Users can:
- Register an account
- Log in securely
- View available movies
- Purchase movie tickets
- Add movies
- Update movie information
- Delete movies
  
#Authentication System:
User credentials are stored in a SQLite database (users.db). Security features include:

- Passwords are securely hashed using bcrypt.
- Username and password validation

#Database:
MySQL Stores:
- Movie information
- Ticket sales records

SQLite Stores:
- User accounts
- Hashed passwords

#Technical tools and libraries:
- Python 3
- TCP socket
- JSON
- MySQL
- Tkinter
- SQLite
- bcrypt
- threading


#Running instructions: Prerequisites: pip install mysql-connector-python bcrypt
Database Setup:
1. Create a new MySQL database.
2. Open the provided SQL file and execute it to create all the required tables and populate the database.
3. Open the MySQL_config.py and update the MySQL connection details. Update the following values:
HOST = "localhost"
PORT = 3306
USER = "your_username"
PASSWORD = "your_password"
DATABASE = "cinema_db"
4. Run the Cinema server.py
5. In a new terminal run Cinema client.py

Login screenshot: 
<img width="1746" height="788" alt="image" src="https://github.com/user-attachments/assets/14a33497-30da-4af4-943a-4f4945bf7b38" />

Register screenshot: 
<img width="1755" height="796" alt="image" src="https://github.com/user-attachments/assets/f59ddd46-0e72-4eb3-bd33-704a476340ef" />

Cinema management system screenshot: 
<img width="1752" height="791" alt="image" src="https://github.com/user-attachments/assets/219fa3b7-c146-489c-9b13-0037cabeaca2" />




