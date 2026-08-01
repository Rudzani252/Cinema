use skyCity_market;
create table user(
name varchar(30));
drop table user;

create table user(
user_id int auto_increment primary key,
full_name varchar(100) not null,
email varchar(100) unique not null,
password VARCHAR(255) NOT NULL, 
shop_name VARCHAR(100), 
neighbourhood VARCHAR(100), 
role_id INT, 
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (role_id) REFERENCES roles(role_id));
 
 CREATE TABLE products (
 product_id INT AUTO_INCREMENT PRIMARY KEY, 
 user_id INT, 
 product_name VARCHAR(100) NOT NULL, 
 description TEXT, price DECIMAL(10,2), 
 image VARCHAR(255), 
 category VARCHAR(100), 
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
 FOREIGN KEY (user_id) REFERENCES users(user_id));
 
 CREATE TABLE cart ( 
 cart_id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT, product_id INT,
 quantity INT DEFAULT 1, 
 FOREIGN KEY (user_id) REFERENCES users(user_id), 
 FOREIGN KEY (product_id) REFERENCES products(product_id));
 
 CREATE TABLE orders ( 
 order_id INT AUTO_INCREMENT PRIMARY KEY, 
 user_id INT, total_price DECIMAL(10,2), 
 order_status VARCHAR(50), 
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES users(user_id));

 