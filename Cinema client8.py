from multiprocessing.resource_tracker import register
from tkinter import *
import tkinter as ttk
import json
import mysql.connector
from tkinter import messagebox
import bcrypt
import re
import sqlite3
import socket



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
        self.show_frame(self.login_frame)

    def register(self):
        username = username1.get()
        password = password1.get()
        if not username:
            return False, print("Username required")

        if len(password) < 8:
            return False, print("Password must be at least 8 character")
        elif not re.search(r"[A-Z]", password):
            return False, print("Password must at least contain a upper letter")
        elif not re.search(r"[a-z]", password):
            return False, print("Password must at least contain a lower letter")
        elif not re.search(r"\d", password):
            return False, print("Password must contain at least one number")
        else:
            try:
                password = "password".encode()
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                c.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, hashed_password))
                conn.commit()
                print("Registered successfully")
            except sqlite3.IntegrityError:
                print("Username already exists")
            except sqlite3.OperationalError:
                print("Database is locked, try again:")
            finally:
                con.close()

    def login(self):
        username = username1.get()

        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()

            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = c.fetchone()

            if not row:
                print("Invalid username")
                return False
            else:
                print("Logged in successfully")

        except sqlite3.OperationalError:
            print("Database is locked, try again:")
        finally:
            conn.close()





    def send_request(self, request_data):
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect(('localhost', 8000))
            c.sendall(json.dumps(request_data).encode())
            response = json.loads(c.recv(4096).decode())
            c.close()
            return response
        except socket.error:
            return {"status": "error"}





    con = mysql.connector.connect(host="127.0.0.1", port="3306 ", user="root",
                                      password="", database="Cinema1")
    cur = con.cursor()

    def add_movie(self):
        try:

            title = entryTitle.get()
            cinema_room = entryRoom.get()
            release_date = entryRel_date.get()
            end_date = entryEnd_date.get()
            tickets_available = entryTick_avali.get()
            ticket_price = entryTick_price.get()

            if not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
                messagebox.showinfo("error, enter invalid inputs")

            else:
                response = send_request({
                    "action": "add_movie",
                    "data": {"movie_id": movie_id, "title": title, "release_date": release_date,
                             "end_date": end_date, "tickets_available": tickets_available,
                             "ticket_price": ticket_price}})
                print("New movie added successfully")
                if response["status"] == "success":
                    messagebox.showinfo("Success", "Movie added")
        except ValueError:
            print("Invalid Input")

            

    def update(self, title, cinema_room, release_date, end_date, tickets_available, ticket_price):
        try:
            title = entryTitle.get()
            cinema_room = entryRoom.get()
            release_date = entryRel_date.get()
            end_date = entryEnd_date.get()
            tickets_available = entryTick_avali.get()
            ticket_price = entryTick_price.get()
        except ValueError:
            print("Invalid Input")

        try:
            if not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
                print("error, enter invalid inputs")
                return
            else:
                response = send_request(
                    {"action": "update_movie",
                     "data": {"movie_id": movie_id, "title": title, "release_date": release_date,
                              "end_date": end_date, "tickets_available": tickets_available,
                              "ticket_price": ticket_price}})
                if response["status"] == "success":
                    messagebox.showinfo("Success", "Movie was updated")
                else:
                    messagebox.showinfo("failed", "movie not updated")
        except ValueError:
            print("Invalid Input")

            

    def delete(self):
        title = entryTitle.get()
        if not title:
            print("Movie not found")
            return
        response = send_request({
            "action": "delete_movie",
            "data": {"movie_id": movie_id}
        })
        if response["status"] == "success":
            messagebox.showinfo("Success", "Movie was deleted")
        else:
            messagebox.showinfo("failed movie not deleted")

            

    def buy_ticket(self):
        con = mysql.connector.connect(host="127.0.0.1", user="root", password=
        "R25190412r", database="Cinema1")
        cur = con.cur()
        try:
            movie_title = entryTitle.get()
            customer_name = entrycust_name.get()
            no_tickets = entrynum_Tick.get()

            cur.execute("SELECT tickets_available FROM Movies WHERE title = %s", (movie_title,))
            movie_tickets = cur.fetchall()
            con.commit()
            if movie_tickets is None:
                print("Movie not found")
            else:
                total_tickets = movie_tickets[0]
                if total_tickets < no_tickets:
                    messagebox.showinfo("No tickets available")
                else:
                    new_total_tickets = total_tickets - no_tickets
                    cur.execute("UPDATE Movies SET tickets_available = %s WHERE title = %s",
                                (new_total_tickets, movie_title))
                    con.commit()
                    print("Tickets updated")
                    con.close()

            cur.execute("SELECT ticket_price FROM Movies WHERE title = %s", (movie_title,))
            results = cur.fetchone()
            con.commit()

            if results is None:
                print("Movie not found")
            else:
                ticket_price = results[0]
                try:
                    cur.execute(
                        "INSERT INTO sales (title,customer_name, number_of_tickets, total ) VALUES(%s, %s, %s, %s)",
                        (movie_title, customer_name, no_tickets, ticket_price))
                    con.commit()

                    messagebox.showinfo("Success", f"{no_tickets} tickets for R{ticket_price}")
                except mysql.connector.errors.IntegrityError:
                    print("Movie already added")
                finally:
                    con.close()

        except ValueError:
            print("Invalid input")
        finally:
            con.close()


    def show_frame(self, frame):
        frame.tkraise()

    def create_login(self):


        username1 = Entry(self.login_frame).place(x=400, y=150, relwidth=0.3, relheight=0.05)
        password1 = Entry(self.login_frame).place(x=400, y=200, relwidth=0.3, relheight=0.05)

        Label(self.login_frame, text="Login",font="Arial90").place(x=570, y=50)
        Label(self.login_frame, text="Username").place(x=390, y=150)
        Label(self.login_frame, text="Password").place(x=390, y=200)

        Button(self.login_frame,text = "Register", command=lambda: self.show_frame(self.register_frame)).place(x =459, y = 300,relwidth=0.06, relheight=0.05)
        Button(self.login_frame, text="Login", command = login ).place(x=620, y=300,relwidth=0.06, relheight=0.05)
        Button(self.login_frame, text="Next",command=lambda: self.show_frame(self.cinema_frame)).place(x=781, y=300, relwidth=0.06, relheight=0.05)

    def create_register(self):
        Label(self.register_frame, text="Register", font="Arial,90").place(x=570, y=50)
        Label(self.register_frame, text="Username").place(x=390, y=150)
        Label(self.register_frame, text="Password").place(x=390, y=200)
        Label(self.register_frame, text="Confirm Password").place(x=390, y=250)

        Entry(self.register_frame).place(x=400, y=150, relwidth=0.3, relheight=0.05)
        Entry(self.register_frame).place(x=400, y=200, relwidth=0.3, relheight=0.05)
        Entry(self.register_frame).place(x=400, y=250, relwidth=0.3, relheight=0.05)

        Button(self.register_frame, text="Register", command= register1).place(x=620, y=300, relwidth=0.06, relheight=0.05)
        Button(self.register_frame, text="Back",command=lambda: self.show_frame(self.login_frame) ).place(x=459, y=300, relwidth=0.06, relheight=0.05)
        Button(self.register_frame, text="Next",command=lambda: self.show_frame(self.cinema_frame)).place(x=781, y=300, relwidth=0.06, relheight=0.05)

    def create_cinema(self):
        Label(self.cinema_frame,text="Movie ID:").place(x=0, y=50)
        Label(self.cinema_frame,text="Title:").place(x=0, y=75)
        Label(self.cinema_frame,text="Room (1-7):").place(x=0, y=100)
        Label(self.cinema_frame,text="Release Date:").place(x=0, y=125)
        Label(self.cinema_frame,text="End Date:").place(x=0, y=150)
        Label(self.cinema_frame,text="Tickets Avail:").place(x=0, y=175)
        Label(self.cinema_frame,text="Ticket Price").place(x=0, y=200)

        # entry field
        Entry(self.cinema_frame).place(x=85, y=50)
        entryTitle= Entry(self.cinema_frame).place(x=85, y=75)
        entryRoom = Entry(self.cinema_frame).place(x=85, y=100)
        entryRel_date= Entry(self.cinema_frame).place(x=85, y=125)
        entryEnd_date= Entry(self.cinema_frame).place(x=85, y=150)
        entryTick_avali= Entry(self.cinema_frame).place(x=85, y=175)
        entryTick_price= Entry(self.cinema_frame).place(x=85, y=200)



        Label(self.cinema_frame,text="Customer Name:").place(x=1000, y=100)
        entryCust_name= Entry(self.cinema_frame,).place(x=1150, y=100)
        Label(self.cinema_frame,text="Number of Tickets:").place(x=1000, y=150)
        entryNum_Tick= Entry(self.cinema_frame).place(x=1150, y=150)
        Label(self.cinema_frame,text="Total:").place(x=1000, y=200)
        entryTotal= Entry(self.cinema_frame).place(x=1150, y=200)
        Label(self.cinema_frame,text="Movie ID:").place(x=1000, y=50)
        Entry(self.cinema_frame).place(x=1150, y=50)
        # Button
        Button(self.cinema_frame,text="Add Movie", command=add_movie, width=15, ).place(x=85, y=300)
        Button(self.cinema_frame, text="Update Movie", command=update, width=15, ).place(x=300, y=300)
        Button(self.cinema_frame, text="Delete Movie", command=delete, width=15, ).place(x=515, y=300)
        Button(self.cinema_frame, text="Buy Ticket", width=15, ).place(x=730, y=300)
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




