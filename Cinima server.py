import mysql.connector
import json
import socket
import threading
from MySQL_config import *





def handle_request(data, ):
   
    connection = mysql.connector.connect(host= HOST, port= PORT,user= USER,
                                         password= PASSWORD ,database=DATABASE)

    try:
        request = json.loads(data)
        action = request.get("action")
        payload = request.get("data", {})
        cursor = connection.cursor()

        if action == "add_movie":
            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_date")
            end_date = payload.get("end_date")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("""INSERT INTO Movies (title, cinema_room, release_date,end_date, tickets_available, ticket_price) VALUES (%s, %s, %s, %s, %s,%s)""",
                           (title, cinema_room, release_date,end_date, tickets_available,ticket_price))
            connection.commit()
            return json.dumps({"status": "success", "message": "Movie added."})


        elif action == "update_movie":
            old_title = payload.get("old_title")

            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_date")
            end_date = payload.get("end_date")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("UPDATE Movies SET  title = %s,cinema_room= %s,release_date= %s, end_date= %s, tickets_available = %s, ticket_price = %s WHERE title = %s """,(
                 title, cinema_room, release_date, end_date, tickets_available, ticket_price, old_title))
            connection.commit()
            return json.dumps({"status": "success",
                               "message": "Movie is updated."})

        elif action == "delete_movie":
            title = payload.get("title")
            cursor.execute("DELETE FROM Movies WHERE title =%s",(title,))
            connection.commit() 
            return json.dumps({"status": "success", "message": f"Movie with Title {title} deleted."})
        
        elif action == "buy_ticket":
            movie_title = payload.get("movie_title")
            customer_name = payload.get("customer_name")
            no_tickets = payload.get("number_of_tickets")
            cursor.execute("SELECT tickets_available FROM Movies WHERE title = %s", (movie_title,))
            movie_tickets = cursor.fetchone()
            

            if movie_tickets is None:
                return json.dumps({"status": "error",
                                   "message": "Movie Unavailable."})
            else:
                total_tickets = movie_tickets[0]
                if total_tickets < no_tickets:
                     return json.dumps({"status": "error",
                                        "message": "Not enough tickets available."})
                else:
                    new_total_tickets = total_tickets - no_tickets
                    cursor.execute("UPDATE Movies SET tickets_available = %s WHERE title = %s",
                                            (new_total_tickets, movie_title))
                    connection.commit()
                    print("Tickets updated")
            cursor.execute("SELECT ticket_price FROM Movies WHERE title = %s", (movie_title,))
            results = cursor.fetchone()
            
            if results is None:
                print("Movie not found")
            else:
                ticket_price = results[0]
                total = ticket_price * no_tickets
                try:
                    cursor.execute(
                                "INSERT INTO sales1 (movie_title,customer_name, number_of_tickets, total ) VALUES(%s, %s, %s, %s)",
                                (movie_title, customer_name, no_tickets,  total))
                    connection.commit()
            
                    return json.dumps({"status": "success","message": "Tickets purchased successfully.","total": float(total)})
                except mysql.connector.errors.IntegrityError:
                    print("Movie already added")




    
        elif action == "get_movies":
            cursor.execute("SELECT * FROM Movies")
            movies = cursor.fetchall()

            return json.dumps({
            "status": "success",
            "movies": movies}, default=str)

        else:
            return json.dumps({ "status": "error", "message": "Unknown action" })

        


    except mysql.connector.OperationalError:
        print("Database is locked, try again:")
    except mysql.connector.IntegrityError:
        print("Movie with title already exists.")
    finally:
        connection.close()



def client_thread(conn, address): 
    print(f"[+] Connected: {address}") 
    try: 
        data = conn.recv(1024).decode() 
        if data: 
            response = handle_request(data, ) 
            conn.sendall(response.encode()) 
    except ValueError: 
        print("Error with address") 
    finally: 
        conn.close() 


def server(): 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind(('localhost', 8000)) 
    s.listen() 
    print('Server listening on port 8000') 

    while True: 
        conn, address = s.accept() 
        threading.Thread(target=client_thread, args=(conn, address)).start() 



server()