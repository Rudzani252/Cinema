import socket
from tkinter import *
from tkinter import ttk
import json
import mysql.connector
from tkinter import messagebox


def send_request(request_data):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(('localhost', 8000))
        c.sendall(json.dumps(request_data).encode())
        response = json.loads(c.recv(4096).decode())
        c.close()
        return response
    except Exception as e:
        return {"status": "error"}






connection = mysql.connector.connect(host="127.0.0.1", user="root", password=
"R25190412r", database="Cinema1")
cursor = connection.cursor()


def add_movie():
    try:

        movie_id = entryMovieId.get()
        title = entryTitle.get()
        cinema_room = entryRoom.get()
        release_date = entryRel_date.get()
        end_date = entryEnd_date.get()
        tickets_available = entryTick_avali.get()
        ticket_price = entryTick_price.get()

        if not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
            print("error, enter invalid inputs")
            return

        response = send_request({
        "action": "add_movie","data": {"movie_id": movie_id, "title": title, "release_date": release_date,
             "end_date": end_date, "tickets_available": tickets_available, "ticket_price": ticket_price}})
        print("New movie added successfully")
        if response["status"] == "success":
            messagebox.showinfo("Success", "Movie added")
    except ValueError:
        print("Invalid Input")


def update():
    title = entryTitle.get()
    cinema_room = entryRoom.get()
    release_date = entryRel_date.get()
    end_date = entryEnd_date.get()
    tickets_available = entryTick_avali.get()
    ticket_price = entryTick_price.get()
    try:
        if not title or not cinema_room or not release_date or not end_date or not tickets_available or not ticket_price:
            print("error, enter invalid inputs")
            return
        response = send_request({"action": "update_movie","data": {"movie_id": movie_id, "title": title, "release_date": release_date,
             "end_date": end_date, "tickets_available": tickets_available, "ticket_price": ticket_price} })
        if response["status"] == "success":
            messagebox.showinfo("Success", "Movie was updated")
        else:
            messagebox.showinfo("failed", "movie not updated")
    except ValueError:
        print("Invalid Input")


def delete():
    movie_id = entryMovieId.get()
    if not movie_id:
        print("invalid input")
        return
    response = send_request({
        "action": "delete_movie",
        "data": {"movie_id": movie_id}
    })
    if response["status"] == "success":
        messagebox.showinfo("Success", "Movie was deleted")
    else:
        messagebox.showinfo("failed movie not deleted")


def buy_ticket():
    connection = mysql.connector.connect(host="127.0.0.1", user="root", password=
    "R25190412r", database="Cinema1")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM movies WHERE movie_id = %s", movie_id)
    movie_tickets = cursor.fetchone()

    if movie_tickets:
        movie_id = entry_Movie_id.get()
        customer_name = entrycust_name.get()
        num_of_tickets = entrynum_Tick.get()
        if num_of_tickets <= movie_tickets:
            cursor.execute("UPDATE movies SET tickets_available = tickets_available - %s WHERE movie_id = %s",
            (num_of_tickets, movie_id))
            total = movie_tickets * num_of_tickets
            cursor.execute("INSERT INTO sales (sale_id, movie_id,customer_name, number_of_tickets, total ) VALUES(?, ?, ?, ?, ?)",
                           (sale_id, movie_id, customer_name, num_of_tickets, total))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", f"{num_of_tickets} tickets for R{total}")

    else:
     messagebox.showinfo("not enough tickets")

application = Tk()
application.title("Cinema")
application.geometry("1400x600")

# labels
labelMovie_id = Label(text="Movie ID:")
labelMovie_id.place(x=0, y=50)
labelTitle = Label(text="Title:")
labelTitle.place(x=0, y=75)
labelRoom = Label(text="Room (1-7):")
labelRoom.place(x=0, y=100)
labelRel_date = Label(text="Release Date:")
labelRel_date.place(x=0, y=125)
labelEnd_date = Label(text="End Date:")
labelEnd_date.place(x=0, y=150)
labelTick_avli = Label(text="Tickets Avail:")
labelTick_avli.place(x=0, y=175)
labelTick_price = Label(text="Ticket Price")
labelTick_price.place(x=0, y=200)

# entry field
entryMovieId = Entry()
entryMovieId.place(x=85, y=50)
entryTitle = Entry()
entryTitle.place(x=85, y=75)
entryRoom = Entry()
entryRoom.place(x=85, y=100)
entryRel_date = Entry()
entryRel_date.place(x=85, y=125)
entryEnd_date = Entry()
entryEnd_date.place(x=85, y=150)
entryTick_avali = Entry()
entryTick_avali.place(x=85, y=175)
entryTick_price = Entry()
entryTick_price.place(x=85, y=200)
movieTable = Label(text="Movie List")
movieTable.grid(row=0, column=0)
movieTable = ttk.Combobox(width=33)
movieTable["values"] = (("Avatar 2", "The Surfer", "The Accountant 2", "Sinners", "Moana 2", "Inside Out 2", "Fast X"),
                        movieTable.grid(row=0, column=1))


labelcust_name = Label(text="Customer Name:")
labelcust_name.place(x=1000, y=100)
entrycust_name = Entry()
entrycust_name.place(x=1150, y=100)
labelnum_Tick = Label(text="Number of Tickets:")
labelnum_Tick.place(x=1000, y=150)
entrynum_Tick = Entry()
entrynum_Tick.place(x=1150, y=150)
labeltotal = Label(text="Total:")
labeltotal.place(x=1000, y=200)
entrytotal = Entry()
entrytotal.place(x=1150, y=200)
label_Movie_id = Label(text="Movie ID:")
label_Movie_id.place(x=1000, y=50)
entry_Movie_id = Entry()
entry_Movie_id.place(x=1150, y=50)
# Button
btnAdd = Button(text="Add Movie", command=add_movie, width=15, )
btnAdd.place(x=85, y=300)
btnUpdate = Button(text="Update Movie", command=update, width=15, )
btnUpdate.place(x=300, y=300)
btnDelete = Button(text="Delete Movie", command=delete, width=15, )
btnDelete.place(x=515, y=300)
btnBuy = Button(text="Buy Ticket", width=15, )
btnBuy.place(x=730, y=300)
##TreeView
table = ttk.Treeview(application, columns=("Id", "Title", "Room", "Release_Date",
                                           "End_Date", "Tickets_Available", "Ticket_Price"), show="headings")
table.heading("Id", text="ID")
table.heading("Title", text="Title")
table.heading("Room", text="Room")
table.heading("Release_Date", text="Release Date")
table.heading("End_Date", text="End Date")
table.heading("Tickets_Available", text="Tickets Available")
table.heading("Ticket_Price", text="Ticket Price")
i = 0

cursor.execute("SELECT * FROM movies")
for ro in cursor:
    table.insert("", i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
i = i + 1
table.place(x=0, y=400)
application.mainloop()

