CREATE DATABASE Cinema;
USE Cinema;

CREATE TABLE Movies(
movie_id INT NOT NULL primary key,
title VARCHAR(50),
cinema_room INT,
release_date varchar(50),
end_date varchar(50),
tickets_available INT,
ticket_price DECIMAL
);

CREATE TABLE Sales(
sale_id INT PRIMARY KEY,
movie_id INT,
customer_name VARCHAR(50),
number_of_tickets INT,
total decimal,
foreign key (movie_id) references Movies(movie_id)
);

INSERT INTO Movies (movie_id, title, cinema_room, release_date, tickets_available, ticket_price)
VALUES
(1,"Avatar 2",3,"2025-01-10", "2025-02-20", 50, 80.0),
    (2,"The Surfer", 2, "2025-06-2", "2025-07-25", 70, 75.0),
    (3, "The Accountant 2", 3, "2025-04-25", "2025-06-26", 60, 70.0),
    (4, "Sinners",4,  "2025-04-17", "2025-06-01", 40, 90.0),
    (5, "Moana 2",5, "2024-11-27", "2025-03-05", 80, 65.0),
    (6, "Inside Out 2",6, "2025-01-25", "2025-03-10", 90, 60.0),
    (7, "Fast X", 5, "2025-01-28", "2025-03-15", 100, 85.0)