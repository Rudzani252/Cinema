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