from multiprocessing.resource_tracker import register
from tkinter import *
from tkinter import ttk
import json
import mysql.connector
from tkinter import messagebox
import bcrypt
import re
import sqlite3
import socket
from MySQL_config import *


class Cinema(Tk):
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    command3 = """CREATE TABLE IF NOT EXISTS
                            users(username, password)"""
    c.execute(command3)
    conn.commit()
    conn.close()

    def __init__(self):
        super().__init__()

        self.title("Cinema")
        self.geometry("1400x600")

        self.login_frame = Frame(self)
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.register_frame = Frame(self)
        self.register_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.cinema_frame = Frame(self)
        self.cinema_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_login()
        self.create_register()
        self.create_cinema()

        self.show_frame(self.login_frame)

    def register(self):

        username = self.username2.get()
        password = self.password2.get()
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        if not username:
            return False, messagebox.showinfo("ERROR","Username required")

        if len(password) < 8:
            return False, messagebox.showinfo("ERROR","Password must be at least 8 character")
        elif not re.search(r"[A-Z]", password):
            return False, messagebox.showinfo("ERROR","Password must at least contain a upper letter")
        elif not re.search(r"[a-z]", password):
            return False, messagebox.showinfo("ERROR","Password must at least contain a lower letter")
        elif not re.search(r"\d", password):
            return False, messagebox.showinfo("ERROR","Password must contain at least one number")
        else:
            try:
                
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                c.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, hashed_password))
                conn.commit()
                messagebox.showerror(
                                "Registered",
                                "Please Login")
            except sqlite3.IntegrityError:
                messagebox.showerror("ERROR","Username already exists")
            except sqlite3.OperationalError:
                print("Database is locked, try again:")
            finally:
                conn.close()

    def login(self):
        username = self.username1.get()
        password = self.password1.get()


        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()

            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = c.fetchone()

            if not row:
                messagebox.showerror("ERROR","Invalid username or passowrd")
                return False
            stored_password = row[0]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode("utf-8")

            if bcrypt.checkpw(password.encode("utf-8"),stored_password):
                messagebox.showerror("Success","Logged in successfully")
                return True
            else:
                messagebox.showerror(
                "Login Failed",
                "Invalid username or password")
                return False

        except sqlite3.OperationalError:
            print("Database is locked, try again:")
        finally:
            conn.close()





    def send_request(self, request_data):
        try:
            print("Connecting to server...")
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect(('localhost', 8000))
            print("Connected to server!")
            c.sendall(json.dumps(request_data).encode())
            response = json.loads(c.recv(4096).decode())
            c.close()
            return response
        except socket.error:
            return {"status": "error"}





    
    

    def add_movie(self):
        try:

            title = self.entryTitle.get()
            cinema_room = int(self.entryRoom.get())
            release_date = self.entryRel_date.get()
            end_date = self.entryEnd_date.get()
            tickets_available = self.entryTick_avali.get()
            ticket_price = self.entryTick_price.get()

            if not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
                messagebox.showinfo("error, enter invalid inputs")

            else:
                response = self.send_request({
                    "action": "add_movie",
                    "data": { "title": title,"cinema_room": cinema_room, "release_date": release_date,
                             "end_date": end_date, "tickets_available": tickets_available,
                             "ticket_price": ticket_price}})
                print("New movie added successfully")
                if response["status"] == "success":
                    messagebox.showinfo("Success", "Movie added")
        except ValueError:
            print("Invalid Input")

            

    def update(self):
        try:
            movie_id = int(self.entryMovie_id.get())
            title = self.entryTitle.get()
            cinema_room = int(self.entryRoom.get())
            release_date = self.entryRel_date.get()
            end_date = self.entryEnd_date.get()
            tickets_available = self.entryTick_avali.get()
            ticket_price = self.entryTick_price.get()
        except ValueError:
            print("Invalid Input")

        try:
            if not movie_id or not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
                print("error, enter invalid inputs")
                return
            else:
                response = self.send_request(
                    {"action": "update_movie",
                     "data": { "movie_id": movie_id,"title": title,"cinema_room": cinema_room, "release_date": release_date,
                              "end_date": end_date, "tickets_available": tickets_available,
                              "ticket_price": ticket_price}})
                if response["status"] == "success":
                    messagebox.showinfo("Success", "Movie was updated")
                else:
                    messagebox.showinfo("failed", "movie not updated")
        except ValueError:
            print("Invalid Input")

            

    def delete(self):
        title = self.entryTitle.get()
        if not title:
            print("Movie not found")
            return
        response = self.send_request({
            "action": "delete_movie",
            "data": {"title": title}
        })
        if response["status"] == "success":
            messagebox.showinfo("Success", "Movie was deleted")
        else:
            messagebox.showinfo("failed movie not deleted")

           

    def buy_ticket(self):
  
        try:
            selected = self.movie_listbox.curselection()
            if not selected:
                print("No Movie Selected\n Please select a movie.")
                return

            
        
            movie_title = self.movie_listbox.get(selected[0])
            customer_name = self.entryCust_name.get()
            no_tickets = int(self.entryNum_Tick.get())

            if not customer_name:
                messagebox.showwarning(
                "Missing Information",
                "Please enter your name.")
                return 
            if no_tickets <= 0:
                messagebox.showwarning(
                "Invalid Number",
                "Please enter a valid number of tickets.")
                return
            response = self.send_request({
            "action": "buy_ticket",
            "data": {
                "movie_title": movie_title,
                "customer_name": customer_name,
                "number_of_tickets": no_tickets
            }})
            if response["status"] == "success":

                total = response["total"]

                messagebox.showinfo(
                "Success",
                f"Tickets purchased successfully!\n\n"
                f"Movie: {movie_title}\n"
                f"Tickets: {no_tickets}\n"
                f"Total: R{total:.2f}")
            else:
                messagebox.showerror(
                "Purchase Failed",
                response.get("message", "Unable to purchase tickets."))           

        except ValueError:
            print("Invalid input")
        


    def show_frame(self, frame):
        frame.tkraise()

    def create_login(self):


        self.username1 = Entry(self.login_frame)
        self.username1.place(x=400, y=150, relwidth=0.3, relheight=0.05)
        self.password1 = Entry(self.login_frame)
        self.password1.place(x=400, y=200, relwidth=0.3, relheight=0.05)

        Label(self.login_frame, text="Login",font="Arial90").place(x=570, y=50)
        Label(self.login_frame, text="Username").place(x=250, y=150)
        Label(self.login_frame, text="Password").place(x=250, y=200)

        Button(self.login_frame,text = "Register", command=lambda: self.show_frame(self.register_frame)).place(x =459, y = 300,relwidth=0.06, relheight=0.05)
        Button(self.login_frame, text="Login", command = self.login ).place(x=620, y=300,relwidth=0.06, relheight=0.05)
        Button(self.login_frame, text="Next",command=lambda: self.show_frame(self.cinema_frame)).place(x=781, y=300, relwidth=0.06, relheight=0.05)

    def create_register(self):
        Label(self.register_frame, text="Register", font="Arial,90").place(x=570, y=50)
        Label(self.register_frame, text="Username").place(x=250, y=150)
        Label(self.register_frame, text="Password").place(x=250, y=200)
        Label(self.register_frame, text="Confirm Password").place(x=250, y=250)

        self.username2 = Entry(self.register_frame)
        self.username2.place(x=400, y=150, relwidth=0.3, relheight=0.05)
        self.password2= Entry(self.register_frame)
        self.password2.place(x=400, y=200, relwidth=0.3, relheight=0.05)
        self.confPass = Entry(self.register_frame)
        self.confPass.place(x=400, y=250, relwidth=0.3, relheight=0.05)

        Button(self.register_frame, text="Register", command= self.register).place(x=620, y=300, relwidth=0.06, relheight=0.05)
        Button(self.register_frame, text="Back",command=lambda: self.show_frame(self.login_frame) ).place(x=459, y=300, relwidth=0.06, relheight=0.05)
        

    def create_cinema(self):
        con = mysql.connector.connect(host=HOST, user=USER, password=
                PASSWORD, database= DATABASE)
        cur = con.cursor()
        Label(self.cinema_frame,text="Movie ID \n(for updates)").place(x=0, y=35)
        Label(self.cinema_frame,text="Title:").place(x=0, y=75)
        Label(self.cinema_frame,text="Title:").place(x=0, y=75)
        Label(self.cinema_frame,text="Room (1-7):").place(x=0, y=100)
        Label(self.cinema_frame,text="Release Date:").place(x=0, y=125)
        Label(self.cinema_frame,text="End Date:").place(x=0, y=150)
        Label(self.cinema_frame,text="Tickets Avail:").place(x=0, y=175)
        Label(self.cinema_frame,text="Ticket Price").place(x=0, y=200)

        # entry field
        self.entryMovie_id= Entry(self.cinema_frame)
        self.entryMovie_id.place(x=85, y=50)
        self.entryTitle= Entry(self.cinema_frame)
        self.entryTitle.place(x=85, y=75)
        self.entryRoom = Entry(self.cinema_frame)
        self.entryRoom.place(x=85, y=100)
        self.entryRel_date= Entry(self.cinema_frame)
        self.entryRel_date.place(x=85, y=125)
        self.entryEnd_date= Entry(self.cinema_frame)
        self.entryEnd_date.place(x=85, y=150)
        self.entryTick_avali= Entry(self.cinema_frame)
        self.entryTick_avali.place(x=85, y=175)
        self.entryTick_price= Entry(self.cinema_frame)
        self.entryTick_price.place(x=85, y=200)



        Label(self.cinema_frame,text="Customer Name:").place(x=1000, y=150)
        self.entryCust_name= Entry(self.cinema_frame,)
        self.entryCust_name.place(x=1150, y=150)

        Label(self.cinema_frame,text="Number of Tickets:").place(x=1000, y=200)
        self.entryNum_Tick= Entry(self.cinema_frame)
        self.entryNum_Tick.place(x=1150, y=200)

        

        Label(self.cinema_frame,text="Select a Movie").place(x=1000, y=50)
        self.movie_listbox = Listbox(self.cinema_frame,width=40,height=5)
        self.movie_listbox.place(x=1150,y=50)
        response = self.send_request({"action": "get_movies","data": {}})
        if response["status"] == "success":
            for movie in response["movies"]:
                self.movie_listbox.insert(END,movie[1]) 
       
        
        # Button
        Button(self.cinema_frame,text="Add Movie", command=self.add_movie, width=15, ).place(x=85, y=300)
        Button(self.cinema_frame, text="Update Movie", command=self.update, width=15, ).place(x=300, y=300)
        Button(self.cinema_frame, text="Delete Movie", command=self.delete, width=15, ).place(x=515, y=300)
        Button(self.cinema_frame, text="Buy Ticket",command=self.buy_ticket, width=15, ).place(x=1150, y=250)
        Button(self.cinema_frame, text="Back",command=lambda: self.show_frame(self.login_frame) ).place(x=0, y=0, relwidth=0.06, relheight=0.05)
        ##TreeView
        table = ttk.Treeview(self.cinema_frame, columns=("Id", "Title", "Room", "Release_Date",
                                                   "End_Date", "Tickets_Available", "Ticket_Price"), show="headings")
        table.heading("Id", text="ID")
        table.heading("Title", text="Title")
        table.heading("Room", text="Room")
        table.heading("Release_Date", text="Release Date")
        table.heading("End_Date", text="End Date")
        table.heading("Tickets_Available", text="Tickets Available")
        table.heading("Ticket_Price", text="Ticket Price")
        i = 0

        cur.execute("SELECT * FROM movies")
        for ro in cur:
            table.insert("", i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
        i = i + 1


        
            
        table.place(x=0, y=400)






if __name__ == '__main__':
    app = Cinema()
    app.mainloop()
