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