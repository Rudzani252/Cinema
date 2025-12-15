import mysql.connector
import json
import socket
import threading





def handle_request(data, ):
   
    connection = mysql.connector.connect(host="127.0.0.1", port= "3306 ",user="root",
                                         password= "R25190412r" ,database="Cinema1")

    try:
        request = json.loads(data)
        action = request.get("action")
        payload = request.get("data", {})
        cursor = connection.cursor()

        if action == "add_movie":
            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_day")
            end_date = payload.get("end_day")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("""INSERT INTO Movies (title, cinema_room, release_date,end_date, tickets_available, ticket_price VALUES (%s, %s, %s, %s, %s,%s)""",
                           (title, cinema_room, release_date,end_date, tickets_available,ticket_price))
            connection.commit()
            return json.dumps({"status": "success", "message": "Movie added."})


        elif action == "update_movie":

            title = payload.get("title")
            cinema_room = payload.get("cinema_room")
            release_date = payload.get("release_day")
            end_date = payload.get("end_day")
            tickets_available = payload.get("tickets_available")
            ticket_price = payload.get("ticket_price")

            cursor.execute("UPDATE Movies SET  title = %s,cinema_room= %s,release_date= % s, end_date= % s, tickets_available = % s, ticket_price = %s WHERE title = %s """,(
                 title, cinema_room, release_date, end_date, tickets_available, ticket_price))
            connection.commit()
            return json.dumps({"movie is updated."})

        elif action == "delete_movie":
            title = payload.get("title")
            cursor.execute("DELETE FROM Movies WHERE title =%s",title)
            connection.commit() 
            return json.dumps({"status": "success", "message": f"Movie with Title {title} deleted."})


    except mysql.connector.OperationalError:
        print("Database is locked, try again:")
    except mysql.connector.IntegrityError:
        print("Movie with title already exists.")
    finally:
        connection.close()



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