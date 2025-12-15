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

    def show_frame(self, frame):
        frame.tkraise()

    def create_login(self):
        username1 = Entry(self.login_frame).place(x=400, y=150, relwidth=0.3, relheight=0.05)
        password1 = Entry(self.login_frame).place(x=400, y=200, relwidth=0.3, relheight=0.05)

        Label(self.login_frame, text="Login", font="Arial90").place(x=570, y=50)
        Label(self.login_frame, text="Username").place(x=390, y=150)
        Label(self.login_frame, text="Password").place(x=390, y=200)

        Button(self.login_frame, text="Register", command=lambda: self.show_frame(self.register_frame)).place(x=459,
                                                                                                              y=300,
                                                                                                              relwidth=0.06,
                                                                                                              relheight=0.05)
        Button(self.login_frame, text="Login", command=login).place(x=620, y=300, relwidth=0.06, relheight=0.05)
        Button(self.login_frame, text="Next", command=lambda: self.show_frame(self.cinema_frame)).place(x=781, y=300,
                                                                                                        relwidth=0.06,
                                                                                                        relheight=0.05)

    def create_register(self):
        Label(self.register_frame, text="Register", font="Arial,90").place(x=570, y=50)
        Label(self.register_frame, text="Username").place(x=390, y=150)
        Label(self.register_frame, text="Password").place(x=390, y=200)
        Label(self.register_frame, text="Confirm Password").place(x=390, y=250)

        Entry(self.register_frame).place(x=400, y=150, relwidth=0.3, relheight=0.05)
        Entry(self.register_frame).place(x=400, y=200, relwidth=0.3, relheight=0.05)
        Entry(self.register_frame).place(x=400, y=250, relwidth=0.3, relheight=0.05)

        Button(self.register_frame, text="Register", command=register1).place(x=620, y=300, relwidth=0.06,
                                                                              relheight=0.05)
        Button(self.register_frame, text="Back", command=lambda: self.show_frame(self.login_frame)).place(x=459, y=300,
                                                                                                          relwidth=0.06,
                                                                                                          relheight=0.05)
        Button(self.register_frame, text="Next", command=lambda: self.show_frame(self.cinema_frame)).place(x=781, y=300,
                                                                                                           relwidth=0.06,
                                                                                                           relheight=0.05)

    def create_cinema(self):
        Label(self.cinema_frame, text="Movie ID:").place(x=0, y=50)
        Label(self.cinema_frame, text="Title:").place(x=0, y=75)
        Label(self.cinema_frame, text="Room (1-7):").place(x=0, y=100)
        Label(self.cinema_frame, text="Release Date:").place(x=0, y=125)
        Label(self.cinema_frame, text="End Date:").place(x=0, y=150)
        Label(self.cinema_frame, text="Tickets Avail:").place(x=0, y=175)
        Label(self.cinema_frame, text="Ticket Price").place(x=0, y=200)

        # entry field
        Entry(self.cinema_frame).place(x=85, y=50)
        entryTitle = Entry(self.cinema_frame).place(x=85, y=75)
        entryRoom = Entry(self.cinema_frame).place(x=85, y=100)
        entryRel_date = Entry(self.cinema_frame).place(x=85, y=125)
        entryEnd_date = Entry(self.cinema_frame).place(x=85, y=150)
        entryTick_avali = Entry(self.cinema_frame).place(x=85, y=175)
        entryTick_price = Entry(self.cinema_frame).place(x=85, y=200)

        Label(self.cinema_frame, text="Customer Name:").place(x=1000, y=100)
        entryCust_name = Entry(self.cinema_frame, ).place(x=1150, y=100)
        Label(self.cinema_frame, text="Number of Tickets:").place(x=1000, y=150)
        entryNum_Tick = Entry(self.cinema_frame).place(x=1150, y=150)
        Label(self.cinema_frame, text="Total:").place(x=1000, y=200)
        entryTotal = Entry(self.cinema_frame).place(x=1150, y=200)
        Label(self.cinema_frame, text="Movie ID:").place(x=1000, y=50)
        Entry(self.cinema_frame).place(x=1150, y=50)
        # Button
        Button(self.cinema_frame, text="Add Movie", command=add_movie, width=15, ).place(x=85, y=300)
        Button(self.cinema_frame, text="Update Movie", command=update, width=15, ).place(x=300, y=300)
        Button(self.cinema_frame, text="Delete Movie", command=delete, width=15, ).place(x=515, y=300)
        Button(self.cinema_frame, text="Buy Ticket", width=15, ).place(x=730, y=300)
        ##TreeView
        table = ttk.Treeview(self.cinema_frame, columns=("Id", "Title", "Room", "Release_Date",
                                                         "End_Date", "Tickets_Available", "Ticket_Price"),
                             show="headings")
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