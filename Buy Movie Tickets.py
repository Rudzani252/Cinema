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