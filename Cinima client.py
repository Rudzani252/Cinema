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
        self.geometry("1400x800")
        self.configure(bg="#F4F5F7")

        self.login_frame = Frame(self, bg="#F4F5F7")
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.register_frame = Frame(self, bg="#F4F5F7")
        self.register_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.cinema_frame = Frame(self, bg="#F4F5F7")
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
                 self.show_frame(self.cinema_frame)
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
                     "data": {"movie_id": movie_id, "title": title,"cinema_room": cinema_room, "release_date": release_date,
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
        # Presentation only: original widget names and callbacks are preserved.
        bg = "#F4F5F7"
        card = "#FFFFFF"
        muted = "#687380"
        white = "#20252B"
        accent = "#39434E"

        Label(self.login_frame, text="CINEMA  /  MANAGEMENT", bg=bg, fg=accent,
              font=("Segoe UI", 12, "bold")).place(x=70, y=42)
        Label(self.login_frame, text="Welcome back.", bg=bg, fg=white,
              font=("Segoe UI", 30, "bold")).place(x=70, y=114)
        Label(self.login_frame, text="Sign in to manage movies and book tickets.", bg=bg, fg=muted,
              font=("Segoe UI", 12)).place(x=72, y=177)

        panel = Frame(self.login_frame, bg=card, width=520, height=490,
                      highlightbackground="#DDE2E7", highlightthickness=1)
        panel.place(x=760, y=125)
        Label(panel, text="Sign in", bg=card, fg=white,
              font=("Segoe UI", 23, "bold")).place(x=52, y=43)
        Label(panel, text="Enter your account details below", bg=card, fg=muted,
              font=("Segoe UI", 11)).place(x=54, y=95)
        Label(panel, text="USERNAME", bg=card, fg=muted,
              font=("Segoe UI", 10, "bold")).place(x=54, y=160)
        self.username1 = Entry(panel, font=("Segoe UI", 13), bg="#F0F2F5", fg=white,
                               insertbackground=white, relief="flat", bd=0)
        self.username1.place(x=54, y=188, width=412, height=43)
        Label(panel, text="PASSWORD", bg=card, fg=muted,
              font=("Segoe UI", 10, "bold")).place(x=54, y=255)
        self.password1 = Entry(panel, font=("Segoe UI", 13), bg="#F0F2F5", fg=white,
                               insertbackground=white, relief="flat", bd=0, show="*")
        self.password1.place(x=54, y=283, width=412, height=43)

        Button(panel, text="Login", command=self.login, font=("Segoe UI", 11, "bold"),
               bg=accent, fg="#FFFFFF", activebackground="#525D69", relief="flat",
               cursor="hand2", bd=0).place(x=54, y=352, width=412, height=44)
        Button(panel, text="Create an account", command=lambda: self.show_frame(self.register_frame),
               font=("Segoe UI", 10, "bold"), bg=card, fg=accent,
               activebackground=card, activeforeground=white, relief="flat", bd=0,
               cursor="hand2").place(x=54, y=411, width=206, height=30)
        

    def create_register(self):
        bg = "#F4F5F7"
        card = "#FFFFFF"
        muted = "#687380"
        white = "#20252B"
        accent = "#39434E"

        Label(self.register_frame, text="CINEMA  /  MANAGEMENT", bg=bg, fg=accent,
              font=("Segoe UI", 12, "bold")).place(x=70, y=42)
        Label(self.register_frame, text="Join the cinema.", bg=bg, fg=white,
              font=("Segoe UI", 30, "bold")).place(x=70, y=114)
        Label(self.register_frame, text="Create an account to explore movies and tickets.",
              bg=bg, fg=muted, font=("Segoe UI", 12)).place(x=72, y=177)

        panel = Frame(self.register_frame, bg=card, width=520, height=545,
                      highlightbackground="#DDE2E7", highlightthickness=1)
        panel.place(x=760, y=95)
        Label(panel, text="Create account", bg=card, fg=white,
              font=("Segoe UI", 23, "bold")).place(x=52, y=32)
        Label(panel, text="Set up your login credentials", bg=card, fg=muted,
              font=("Segoe UI", 11)).place(x=54, y=84)

        Label(panel, text="USERNAME", bg=card, fg=muted,
              font=("Segoe UI", 10, "bold")).place(x=54, y=137)
        self.username2 = Entry(panel, font=("Segoe UI", 13), bg="#F0F2F5", fg=white,
                               insertbackground=white, relief="flat", bd=0)
        self.username2.place(x=54, y=162, width=412, height=41)
        Label(panel, text="PASSWORD", bg=card, fg=muted,
              font=("Segoe UI", 10, "bold")).place(x=54, y=225)
        self.password2 = Entry(panel, font=("Segoe UI", 13), bg="#F0F2F5", fg=white,
                               insertbackground=white, relief="flat", bd=0, show="*")
        self.password2.place(x=54, y=250, width=412, height=41)
        Label(panel, text="CONFIRM PASSWORD", bg=card, fg=muted,
              font=("Segoe UI", 10, "bold")).place(x=54, y=313)
        self.confPass = Entry(panel, font=("Segoe UI", 13), bg="#F0F2F5", fg=white,
                              insertbackground=white, relief="flat", bd=0, show="*")
        self.confPass.place(x=54, y=338, width=412, height=41)

        Button(panel, text="Register", command=self.register,
               font=("Segoe UI", 11, "bold"), bg=accent, fg="#FFFFFF",
               activebackground="#525D69", relief="flat", bd=0,
               cursor="hand2").place(x=54, y=412, width=412, height=44)
        Button(panel, text="← Back to login", command=lambda: self.show_frame(self.login_frame),
               font=("Segoe UI", 10, "bold"), bg=card, fg=accent,
               activebackground=card, activeforeground=white, relief="flat", bd=0,
               cursor="hand2").place(x=54, y=481, width=180, height=30)

    def create_cinema(self):
        con = mysql.connector.connect(host=HOST, user=USER, password=
                PASSWORD, database=DATABASE)
        cur = con.cursor()

        bg = "#F4F5F7"
        card = "#FFFFFF"
        white = "#20252B"
        muted = "#687380"
        accent = "#39434E"
        green = "#414B56"
        red = "#E9D5D8"

        Label(self.cinema_frame, text="CINEMA  /  MANAGEMENT", bg=bg, fg=accent,
              font=("Segoe UI", 11, "bold")).place(x=48, y=25)
        Label(self.cinema_frame, text="Movie dashboard", bg=bg, fg=white,
              font=("Segoe UI", 26, "bold")).place(x=48, y=58)
        Label(self.cinema_frame, text="Manage your movie catalogue and ticket bookings",
              bg=bg, fg=muted, font=("Segoe UI", 11)).place(x=50, y=106)
        Button(self.cinema_frame, text="← Back", command=lambda: self.show_frame(self.login_frame),
               font=("Segoe UI", 10, "bold"), bg=card, fg=white, relief="flat",
               bd=0, cursor="hand2", activebackground="#DDE2E7",
               activeforeground=white).place(x=1240, y=47, width=110, height=38)

        movie_panel = Frame(self.cinema_frame, bg=card, width=730, height=290,
                            highlightbackground="#DDE2E7", highlightthickness=1)
        movie_panel.place(x=48, y=152)
        Label(movie_panel, text="Movie details", bg=card, fg=white,
              font=("Segoe UI", 17, "bold")).place(x=24, y=17)
        Label(movie_panel, text="Add, update or remove a movie", bg=card, fg=muted,
              font=("Segoe UI", 10)).place(x=25, y=52)

        form_fields = [
            ("Movie ID (updates)", 24, 91, "entryMovie_id"),
            ("Title", 380, 91, "entryTitle"),
            ("Room (1–7)", 24, 152, "entryRoom"),
            ("Release Date", 380, 152, "entryRel_date"),
            ("End Date", 24, 213, "entryEnd_date"),
            ("Tickets Available", 380, 213, "entryTick_avali"),
        ]
        for title, x, y, attr in form_fields:
            Label(movie_panel, text=title, bg=card, fg=muted,
                  font=("Segoe UI", 9, "bold")).place(x=x, y=y)
            entry = Entry(movie_panel, bg="#F0F2F5", fg=white,
                          insertbackground=white, font=("Segoe UI", 11),
                          relief="flat", bd=0)
            entry.place(x=x, y=y + 23, width=315, height=32)
            setattr(self, attr, entry)

        # Ticket price uses the same original attribute, placed in the action row.
        Label(self.cinema_frame, text="Ticket Price", bg=bg, fg=muted,
              font=("Segoe UI", 9, "bold")).place(x=48, y=459)
        self.entryTick_price = Entry(self.cinema_frame, bg="#F0F2F5", fg=white,
                                     insertbackground=white, font=("Segoe UI", 11), relief="flat", bd=0)
        self.entryTick_price.place(x=48, y=482, width=155, height=35)

        booking_panel = Frame(self.cinema_frame, bg=card, width=524, height=290,
                              highlightbackground="#DDE2E7", highlightthickness=1)
        booking_panel.place(x=802, y=152)
        Label(booking_panel, text="Book tickets", bg=card, fg=white,
              font=("Segoe UI", 17, "bold")).place(x=24, y=17)
        Label(booking_panel, text="Choose a movie and complete your booking", bg=card, fg=muted,
              font=("Segoe UI", 10)).place(x=25, y=52)
        Label(booking_panel, text="SELECT A MOVIE", bg=card, fg=muted,
              font=("Segoe UI", 9, "bold")).place(x=24, y=88)
        self.movie_listbox = Listbox(booking_panel, bg="#F0F2F5", fg=white,
                                     selectbackground="#C5CDD5", selectforeground="#20252B",
                                     font=("Segoe UI", 10), relief="flat", bd=0,
                                     highlightthickness=0, activestyle="none")
        self.movie_listbox.place(x=24, y=111, width=220, height=109)
        response = self.send_request({"action": "get_movies", "data": {}})
        if response["status"] == "success":
            for movie in response["movies"]:
                self.movie_listbox.insert(END, movie[1])

        Label(booking_panel, text="CUSTOMER NAME", bg=card, fg=muted,
              font=("Segoe UI", 9, "bold")).place(x=262, y=88)
        self.entryCust_name = Entry(booking_panel, bg="#F0F2F5", fg=white,
                                    insertbackground=white, font=("Segoe UI", 11), relief="flat", bd=0)
        self.entryCust_name.place(x=262, y=111, width=230, height=35)
        Label(booking_panel, text="NUMBER OF TICKETS", bg=card, fg=muted,
              font=("Segoe UI", 9, "bold")).place(x=262, y=157)
        self.entryNum_Tick = Entry(booking_panel, bg="#F0F2F5", fg=white,
                                   insertbackground=white, font=("Segoe UI", 11), relief="flat", bd=0)
        self.entryNum_Tick.place(x=262, y=180, width=230, height=35)
        Button(booking_panel, text="Buy Ticket", command=self.buy_ticket,
               font=("Segoe UI", 11, "bold"), bg=accent, fg="#FFFFFF", relief="flat",
               bd=0, cursor="hand2", activebackground="#525D69").place(x=262, y=236, width=230, height=37)

        Button(self.cinema_frame, text="+ Add Movie", command=self.add_movie,
               font=("Segoe UI", 10, "bold"), bg=green, fg="#FFFFFF", relief="flat",
               bd=0, cursor="hand2").place(x=243, y=480, width=155, height=38)
        Button(self.cinema_frame, text="Update Movie", command=self.update,
               font=("Segoe UI", 10, "bold"), bg="#E3E7EB", fg=white, relief="flat",
               bd=0, cursor="hand2").place(x=412, y=480, width=155, height=38)
        Button(self.cinema_frame, text="Delete Movie", command=self.delete,
               font=("Segoe UI", 10, "bold"), bg=red, fg="#20252B", relief="flat",
               bd=0, cursor="hand2").place(x=581, y=480, width=155, height=38)

        Label(self.cinema_frame, text="Movie catalogue", bg=bg, fg=white,
              font=("Segoe UI", 17, "bold")).place(x=48, y=547)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Cinema.Treeview", background=card, foreground=white,
                        fieldbackground=card, rowheight=32, borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Cinema.Treeview.Heading", background="#DDE2E7", foreground=white,
                        relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Cinema.Treeview", background=[("selected", "#D6DCE3")],
                  foreground=[("selected", "#20252B")])
        style.map("Cinema.Treeview.Heading", background=[("active", "#E3E7EB")])

        table = ttk.Treeview(self.cinema_frame, columns=("Id", "Title", "Room", "Release_Date",
                                                   "End_Date", "Tickets_Available", "Ticket_Price"),
                             show="headings", style="Cinema.Treeview")
        table.heading("Id", text="ID")
        table.heading("Title", text="Title")
        table.heading("Room", text="Room")
        table.heading("Release_Date", text="Release Date")
        table.heading("End_Date", text="End Date")
        table.heading("Tickets_Available", text="Tickets Available")
        table.heading("Ticket_Price", text="Ticket Price")
        table.column("Id", width=70, anchor="center")
        table.column("Title", width=285)
        table.column("Room", width=100, anchor="center")
        table.column("Release_Date", width=190, anchor="center")
        table.column("End_Date", width=190, anchor="center")
        table.column("Tickets_Available", width=180, anchor="center")
        table.column("Ticket_Price", width=150, anchor="center")
        i = 0
        cur.execute("SELECT * FROM movies")
        for ro in cur:
            table.insert("", i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
        i = i + 1
        table.place(x=48, y=592, width=1278, height=177)






if __name__ == '__main__':
    app = Cinema()
    app.mainloop()
