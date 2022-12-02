CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Chigozie12@';

CREATE DATABASE auth;


GRANT ALL PRIVILEGES on auth.* TO 'auth_user'@'localhost';

USE auth

CREATE TABLE `user` (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);
 


INSERT INTO user (email, password) VALUES ('chigozie@gmail.com', 'password');