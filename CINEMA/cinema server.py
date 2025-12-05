import mysql.connector
import json
import socket
import threading


def handle_request(data, ):
    connection = mysql.connector.connect(host="127.0.0.1", user="root",
                                         password="R25190412r", database="Cinema1")

    try:
        request = json.loads(data)
        action = request.get("action")
        payload = request.get("data", {})
        cursor = connection.cursor()

        if action == "add_movie":
            movie_id = payload.get("movie_id")
            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_day")
            end_date = payload.get("end_day")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("""INSERT INTO movies (movie_id, title, cinema_room, release_date, 
end_date, tickets_avilable, ticket_price VALUES (%s, %s, %s, %s, %s, %s,%s)""", (movie_id,
                                                                                 title, cinema_room, release_date,
                                                                                 end_date, tickets_available,
                                                                                 ticket_price))
            connection.commit()
            return json.dumps({"status": "success", "message": "Movie added."})


        elif action == "update_movie":
            movie_id = payload.get("movie_id")
            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_day")
            end_date = payload.get("end_day")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("UPDATE movies SET movie_id = %s, title = %s,cinema_room= %s,release_date= % s, end_date= % s, tickets_avilable = % s, ticket_price = %s WHERE movie_id = %s """,(
                movie_id, title, cinema_room, release_date, end_date, tickets_available, 
ticket_price)) 
            connection.commit() 
            return json.dumps({"movie is updated."}) 

        elif action == "delete_movie": 
            movie_id = payload.get("movie_id") 
            cursor.execute("DELETE FROM movies WHERE movie_id=%s",movie_id) 
            connection.commit() 
            return json.dumps({"status": "success", "message": f"Movie with ID {movie_id} deleted."})






    except ValueError: 
        print("invalid input") 


def client_thread(conn, address, connection): 
    print(f"[+] Connected: {address}") 
    try: 
        data = conn.recv(1024).decode() 
        if data: 
            response = handle_request(data, ) 
            conn.sendall(response.encode()) 
    except ValueError: 
        print("Error with address") 
    finally: 
        connection.close() 


def server(): 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind(('localhost', 8000)) 
    s.listen() 
    print('Server listening on port 8000') 

    while True: 
        conn, address = s.accept() 
        threading.Thread(target=client_thread, args=(conn, address)).start() 


server()